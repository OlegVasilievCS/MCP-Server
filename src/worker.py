from typing import TypedDict, List
from langgraph.graph import StateGraph
import os
from dotenv import load_dotenv
from src.mcp_tools import mcp, search_emails, create_jira_issue
from src.ms_auth import MicrosoftAuth
import src.mcp_tools as mcp_module
from groq import Groq
from datetime import date
load_dotenv()




def is_email_a_task(emails):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)


    chat_completion = client.chat.completions.create(
    messages=[
            {
            "role": "user",
            "content": f"Bases on these {emails} tell me shotly if the are a task for me to complete",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print(f"is_email_a_task: ", chat_completion.choices[0].message.content)



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
    today = date.today().strftime('%Y-%m-%d')
    query_string = f"isread:false received:{today}"

    results = search_emails(query=query_string, count=3)
    is_email_a_task(results)
    state["emails"] = results
    state["messages"].append(f"System: Fetched {len(results)} emails")
    return state

def ai_create_jira_issue(state: ChatState) -> ChatState:
    jira_issue = create_jira_issue(state["emails"][0]["subject"], state["emails"][0]["snippet"])
    state["messages"].append(f"Jira issue added: {jira_issue}")
    return state


#     @mcp.tool()
# def create_jira_issue(summary: str, description: str):
#     """Creates a new Jira task."""
#     logger.info(f"Creating Jira task: {summary}")
#     return jira.create_issue(summary, description)


graph = StateGraph(ChatState)
graph.add_node("fetch_emails", email_fetching_node)
graph.add_node("create_issue", ai_create_jira_issue)

graph.add_edge("fetch_emails", "create_issue")
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