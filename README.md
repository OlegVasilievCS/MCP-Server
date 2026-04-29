Enterprise AI Bridge (MCP)

A Model Context Protocol (MCP) server designed to bridge the gap between AI agents (like Claude Desktop) and enterprise productivity suites. This server enables AI to interact securely with Microsoft 365 and Atlassian Jira, allowing for automated workflows that span communication and project management.

Key Features
Jira Automation: Create, list, and manage issues directly from conversation context.

Microsoft Graph Integration: Search and send emails via Office 365 using KQL (Keyword Query Language).

Secure OAuth Flow: Implements MSAL (Microsoft Authentication Library)


Tech Stack
Language: Python 3.10+

Framework: FastMCP

APIs: Microsoft Graph API, Jira REST API

Libraries: msal, atlassian-python-api, requests, python-dotenv

Setup & Installation
Clone the Repository:

Bash
git clone https://github.com/OlegVasilievCS/MCP-Server.git
cd MCP-Server
Install Dependencies:

Bash
pip install -r requirements.txt
Environment Configuration:
Create a .env file in the root directory and add your credentials:

Code snippet
AZURE_CLIENT_ID=your_azure_id
JIRA_URL=https://your-site.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_atlassian_api_token
Authentication:
Run the application manually once to trigger the interactive Microsoft login and cache your token:

Bash
python main.py

Usage Examples
Once connected to Claude Desktop, you can perform complex workflows such as:

"Check my emails for any bug reports from today."

"I found a bug in the latest email. Create a Jira task in project KAN with the summary 'Fix Login Bug' and add the email snippet to the description."

"List my current Jira projects to see where I should add this task."
