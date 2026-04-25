# Microsoft Graph MCP Server

A Model Context Protocol (MCP) server that allows AI agents (like Claude Desktop) to interact with Microsoft 365.

## Features
- **Secure Auth:** Uses MSAL with local token caching.
- **FastMCP:** Built with the lightweight FastMCP framework.

## Setup
1. Clone the repo.
2. Create a `.env` file with your `AZURE_CLIENT_ID`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run manually once to authenticate: `python server.py`
5. Configure your MCP client (e.g., Claude Desktop).
