# src/ms_tools.py
import requests
from mcp.server.fastmcp import FastMCP
from .ms_auth import MicrosoftAuth
from .jira_tools import JiraBridge
import logging
import sys

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
                    stream=sys.stderr)

logger = logging.getLogger("EnterpriseBridge")
mcp = FastMCP("Enterprise-Bridge")

ms_auth = None 
jira = JiraBridge()

@mcp.tool()
def search_emails(query: str, count: int = 5):
    """Searches Office 365 inbox using KQL."""
    logger.info(f"Searching emails for: {query}")
    
    if ms_auth is None:
        logger.error("ms_auth is not initialized!")
        return "Error: Microsoft Auth not initialized."

    token = ms_auth.get_token()
    if not token:
        return "Error: Could not get access token. Check console for login prompt."

    url = f"https://graph.microsoft.com/v1.0/me/messages?$search=\"{query}\"&$top={count}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    logger.info(f"Graph API Status: {response.status_code}")
    if response.status_code == 200:
        emails = response.json().get("value", [])
        return [{"subject": e["subject"], "sender": e["from"]["emailAddress"]["address"], "snippet": e["bodyPreview"]} for e in emails]
    return f"Error: {response.status_code}"

@mcp.tool()
def delete_jira_task(issue_key: str):
    """Deletes a Jira issue by its key (e.g., 'KAN-7')."""
    logger.info(f"Deleting Jira task: {issue_key}")
    return jira.delete_task(issue_key)

@mcp.tool()
def assign_jira_task(issue_key: str, account_id: str):
    """Assign a Jira issue by its key (e.g., 'KAN-7') and account id."""
    logger.info(f"Assigning Jira task: {issue_key} with id: {account_id}")
    return jira.assign_task(issue_key, account_id)

@mcp.tool()
def create_jira_task(summary: str, description: str):
    """Creates a new Jira task."""
    logger.info(f"Creating Jira task: {summary}")
    return jira.create_task(summary, description)

@mcp.tool()
def get_jira_context():
    """Returns available Jira projects and keys."""
    logger.info("Fetching Jira project context")
    return jira.list_projects()

@mcp.tool()
def list_jira_tasks():
    """Lists Jira tasks assigned to the current user that are not yet completed."""
    logger.info("Fetching assigned Jira tasks...")
    return jira.list_my_tasks()