import msal
import requests
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from atlassian import Jira

load_dotenv()

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AUTHORITY = "https://login.microsoftonline.com/common"
# SCOPES = ["Mail.Read", "Mail.Send", "Chat.Read"]
SCOPES = ["Mail.Read", "Mail.Send"]

JIRA_URL = "https://oleg-dev-projects.atlassian.net"
JIRA_EMAIL = "voleg239@gmail.com"
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

jira = Jira (
    url=JIRA_URL,
    username=JIRA_EMAIL,
    password=JIRA_API_TOKEN,
    cloud=True
)

mcp = FastMCP("Oleg-MCP")


@mcp.tool()
def create_jira_task(summary: str, description: str):
    """Creates a new task in the Jira backlog."""
    try:
        issue_dict = {
            'project': {'key': 'KAN'}, 
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Task'}, 
        }
        new_issue = jira.create_issue(fields=issue_dict)
        return f"Success! Ticket created: {new_issue['key']}"
    except Exception as e:
        return f"Jira Technical Error: {str(e)}"

def get_ms_token():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(base_dir, "token_cache.bin")
    
    cache = msal.SerializableTokenCache()
    
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        CLIENT_ID, 
        authority=AUTHORITY, 
        token_cache=cache
    )

    accounts = app.get_accounts()
    result = None

    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        print("No valid token found. Opening browser for interactive login...")
        result = app.acquire_token_interactive(scopes=SCOPES, prompt="consent")
        
    if result and 'access_token' in result:
        with open(cache_path, "w") as f:
            f.write(cache.serialize())
        return result['access_token']

    return None


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


@mcp.tool()
def send_email(email_subject: str, email_content: str, recipient_email: str):
    """
    Sends a plain text email to a specified recipient.
    :param recipient_email: The email address of the person to receive the mail.
    :param email_subject: The subject line of the email.
    :param email_content: The body text of the email.
    """
    token = get_ms_token()

    if not token:
        return "Error: Could not retrieve access token. Try deleting token_cache.bin and restarting."

    url = "https://graph.microsoft.com/v1.0/me/sendMail"

    
    request_body = {
        "message": {
            "subject": email_subject,
            "body": {
                "contentType": "Text",
                "content": email_content
            },
            "toRecipients": [ 
                {
                    "emailAddress": {
                        "address": recipient_email
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code == 202:
        return f"Email successfully sent to {recipient_email}!"
    
    return f"Error: {response.status_code} - {response.text}"


@mcp.tool()
def search_emails(query: str, count: int = 5):
    """
    Searches the user's Office 365 inbox. 
    The query supports KQL (Keyword Query Language), 
    e.g., 'from:Microsoft' or 'isread:false'.
    """
    token = get_ms_token()
    url = f"https://graph.microsoft.com/v1.0/me/messages?$search=\"{query}\"&$top={count}"
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        emails = response.json().get("value", [])
        return [{"subject": e["subject"], "snippet": e["bodyPreview"]} for e in emails]
    return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()
    # print("Manual Token Generation...")
    # print(get_ms_token())