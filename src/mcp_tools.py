# src/ms_tools.py
import requests
from mcp.server.fastmcp import FastMCP
from .ms_auth import MicrosoftAuth
from .jira_tools import JiraBridge
import logging
import sys
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
                    stream=sys.stderr)

tvly_API_Client_KEY = os.getenv("tvly_API_KEY")

logger = logging.getLogger("EnterpriseBridge")
mcp = FastMCP("Enterprise-Bridge")
tavily_client = TavilyClient(api_key=tvly_API_Client_KEY)

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
def add_ai_research_summary_to_issue_comment(issue_key: str, research_topic: str):
    """Researches a technical solution and adds it to a Jira issue.
    - issue_key: The Jira ID (e.g., 'KAN-13')
    - research_topic: What to search for (e.g., 'Leo Messi')
    """
    raw_result = tavily_client.search(query=research_topic)
    first_result = raw_result.get('results', [{}])[0].get('content', 'No data found')
    logger.info(f"Adding technical summary: {first_result}")
    return jira.add_research_comment(issue_key, first_result)


@mcp.tool()
def get_all_jira_issues(project: str):
    """Returns a list of all issues for a given project key (e.g., 'KAN')."""
    logger.info(f"Returning all issues for project: {project}")
    return jira.get_all_issues(project)

@mcp.tool()
def delete_jira_issue(issue_key: str):
    """Deletes a Jira issue by its key (e.g., 'KAN-7')."""
    logger.info(f"Deleting Jira task: {issue_key}")
    return jira.delete_issue(issue_key)

@mcp.tool()
def assign_jira_issue(issue_key: str, account_id: str):
    """Assign a Jira issue by its key (e.g., 'KAN-7') and account id."""
    logger.info(f"Assigning Jira task: {issue_key} with id: {account_id}")
    return jira.assign_issue(issue_key, account_id)

@mcp.tool()
def create_jira_issue(summary: str, description: str):
    """Creates a new Jira task."""
    logger.info(f"Creating Jira task: {summary}")
    return jira.create_issue(summary, description)

@mcp.tool()
def get_jira_context():
    """Returns available Jira projects and keys."""
    logger.info("Fetching Jira project context")
    return jira.list_projects()

@mcp.tool()
def list_jira_issues():
    """Lists Jira tasks assigned to the current user that are not yet completed."""
    logger.info("Fetching assigned Jira tasks...")
    return jira.list_my_issues()