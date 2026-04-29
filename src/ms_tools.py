import requests
from mcp.server.fastmcp import FastMCP
from .ms_auth import MicrosoftAuth
from .jira_tools import JiraBridge

mcp = FastMCP("Enterprise-Bridge")

ms_auth = None 
jira = JiraBridge()

@mcp.tool()
def search_emails(query: str, count: int = 5):
    """Searches Office 365 inbox using KQL (Keyword Query Language)."""
    token = ms_auth.get_token()
    url = f"https://graph.microsoft.com/v1.0/me/messages?$search=\"{query}\"&$top={count}"
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        emails = response.json().get("value", [])
        return [{"subject": e["subject"], "sender": e["from"]["emailAddress"]["address"], "snippet": e["bodyPreview"]} for e in emails]
    return f"Error: {response.status_code}"

@mcp.tool()
def create_jira_task(summary: str, description: str):
    """Creates a new Jira task. Useful for converting emails or chats into work items."""
    return jira.create_task(summary, description)

@mcp.tool()
def get_jira_context():
    """Returns available Jira projects and keys to ensure correct task placement."""
    return jira.list_projects()

# @mcp.tool()
# def list_teams_chats(count: int = 10):
#     """
#     Lists the user's most recent Microsoft Teams chats.
#     """
#     token = get_ms_token()
#     if not token:
#         return "Error: Access token missing."

#     headers = {"Authorization": f"Bearer {token}"}
#     url = f"https://graph.microsoft.com/v1.0/me/chats?$top={count}&$orderby=lastMessagePreview/createdDateTime desc"
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         chats = response.json().get("value", [])
#         if not chats:
#             return "No Teams chats found."
            
#         output = []
#         for c in chats:
#             name = c.get("topic") or "One-on-One / Group Chat"
#             chat_id = c.get("id")
#             output.append(f"Chat Name: {name} | ID: {chat_id}")
            
#         return "\n".join(output)
    
#     return f"Error: {response.status_code} - {response.text}"