import os
from dotenv import load_dotenv
from src.ms_tools import mcp, MicrosoftAuth
import src.ms_tools as mcp_module

def main():
    load_dotenv()
    
    client_id = os.getenv("AZURE_CLIENT_ID")
    mcp_module.ms_auth = MicrosoftAuth(client_id)
    
    mcp.run()

if __name__ == "__main__":
    main()