import os
from dotenv import load_dotenv
from src.mcp_tools import mcp, MicrosoftAuth
import src.mcp_tools as mcp_module

load_dotenv()

def main():
    
    client_id = os.getenv("AZURE_CLIENT_ID")
    mcp_module.ms_auth = MicrosoftAuth(client_id)
    
    
    mcp_module.logger.info("Server is initialized and listening...")
    
    mcp.run()

if __name__ == "__main__":
    main()