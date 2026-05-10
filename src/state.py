import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display

load_dotenv()

groq_key = os.getenv("groq_api_key")
lang_smith_key= os.getenv("lang_smith_api_key")

os.environ["LANGCHAIN_API_KEY"] = lang_smith_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "MCP-Server-Email-Reader"


class State(TypedDict):
    # Messages of are of type 'list'. The add_messages appends each message to
    #  the list, instead of overwritng. 
    messages: Annotated[list, add_messages]   

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": llm.invoke(state['messages'])}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "q"]:
#         print("Good Bye")
#         break
#     for event in graph.stream({'messages': ("user", user_input)}):
#         print(event.values())
#         for value in event.values():
#             print(value['messages'])
#             print("Assistant:", value["messages"].content)
