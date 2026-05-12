from typing import TypedDict, List
from langgraph.graph import StateGraph
import os
from dotenv import load_dotenv
from src.mcp_tools import mcp, search_emails
from src.ms_auth import MicrosoftAuth
import src.mcp_tools as mcp_module

load_dotenv()

client_id = os.getenv("AZURE_CLIENT_ID")
mcp_module.ms_auth = MicrosoftAuth(client_id)

class ChatState(TypedDict):
    messages: List[str]
    found_tasks: List[dict]
    emails: List[dict]
    research_summary: str

def user_input_node(state: ChatState) -> ChatState:
    user_message = input("You: ")
    state["messages"].append(f"User: {user_message}")
    return state

def agent_response_node(state: ChatState) -> ChatState:
    last_message = state["messages"][-1]
    reply = f"I see you said, '{last_message.split(': ')[1]}'"
    state["messages"].append(f"Agent: {reply}")
    return state

def email_fetching_node(state: ChatState) -> ChatState:
    results = search_emails(query="Allez Up", count=3)
    state["emails"] = results
    state["messages"].append(f"System: Fetched {len(results)} emails")
    return state


graph = StateGraph(ChatState)
graph.add_node("fetch_emails", email_fetching_node)
# graph.add_node("respond", agent_response_node)

# graph.add_edge("fetch_emails", "respond")
graph.set_entry_point("fetch_emails")

app = graph.compile()
state = {
    "emails": [],
    "messages": [],
    "found_tasks": [],
    "research_summary": ""
}

for _ in range(1):
    state = app.invoke(state)
    print(state)