import msal
import requests
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Mail.Read"]

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
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result: return result['access_token']

    return None

mcp = FastMCP("Oleg-MCP")

@mcp.tool()
def search_emails(query: str, count: int = 5):
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