
from mcp.server.fastmcp import FastMCP


mcp = FastMcp("mcp_sever")


GRAPH         = "https://graph.microsoft.com/v1.0"



@mcp.tool()
def list_emails(top: int = 10) -> str:
    """List my most recent emails."""
    user  = get_current_user()
    token = get_token_for_user(user)
    resp  = requests.get(
        f"{GRAPH}/users/{user}/messages",   
        headers=headers(token),
        params={"$top": top, "$select": "subject,from,receivedDateTime,isRead"},
        timeout=30
    )
    resp.raise_for_status()
    msgs   = resp.json().get("value", [])
    result = [
        {"subject": m["subject"], "from": m["from"]["emailAddress"]["address"],
         "received": m["receivedDateTime"], "read": m["isRead"]}
        for m in msgs
    ]
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run()