**Enterprise AI Bridge (MCP)**

A Model Context Protocol (MCP) server designed to bridge the gap between AI agents (like Claude Desktop) and enterprise productivity suites. 

This server enables AI to interact securely with Microsoft 365 and Atlassian Jira, allowing for automated workflows that span communication and project management.

**Key Features**
Jira Automation: Create, list, and manage issues directly from conversation context.

Autonomous Research (Tavily AI): Automatically research technical solutions and enrich Jira tickets with live web documentation.

Microsoft Graph Integration: Search and send emails via Office 365 using KQL (Keyword Query Language).

Secure OAuth Flow: Implements MSAL (Microsoft Authentication Library) for enterprise-grade security.

**Tavily**

Unlike standard AI implementations that rely solely on a model's internal training data, this bridge integrates Tavily AI.

I integrated Tavily instead of relying only on Claude's internal knowledge for three reasons:

**Real-Time Accuracy:** Software documentation changes weekly. Tavily allows the agent to fetch the current state of libraries (like FastAPI or React) rather than relying on Claude's training cutoff.

**Hallucination Prevention:** By providing "ground truth" search results as context, the agent is significantly less likely to invent non-existent code parameters or API endpoints.

**Verified Sources:** Every technical summary added to a Jira ticket can be backed by live links, providing a clear audit trail for developers.

**Tech Stack**

Language: Python 3.10+

Framework: FastMCP

APIs: Microsoft Graph API, Jira REST API, Tavily Search API

Libraries: msal, atlassian-python-api, tavily-python, requests, python-dotenv

**Setup & Installation**
Clone the Repository:

Bash
git clone https://github.com/OlegVasilievCS/MCP-Server.git
cd MCP-Server
Install Dependencies:

Bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration:**
    Create a `.env` file in the root directory and add your credentials:
    
```env
    AZURE_CLIENT_ID=your_azure_id
    JIRA_URL=https://your-site.atlassian.net
    JIRA_EMAIL=your-email@example.com
    JIRA_API_TOKEN=your_atlassian_api_token
    tvly_API_KEY=your_tavily_api_token
    ```

4.  **Authentication:**
    Run the application manually once to trigger the interactive Microsoft login:
    ```bash
    python main.py
    
    ```
```


**Usage Examples**

"Check my emails for any bug reports from today."

"I found an authentication bug in the latest email. **Research a fix** and create a Jira task in KAN with the research findings added as a comment."

"List my current tasks and use Tavily to find documentation for the highest priority one."
