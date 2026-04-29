import msal
import os

class MicrosoftAuth:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.authority = "https://login.microsoftonline.com/common"
        self.scopes = ["Mail.Read", "Mail.Send"]
        # self.scopes == ["Mail.Read", "Mail.Send", "Chat.Read"]

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cache_path = os.path.join(self.base_dir, "token_cache.bin")
        
        self.cache = msal.SerializableTokenCache()
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as f:
                self.cache.deserialize(f.read())

        self.app = msal.PublicClientApplication(
            self.client_id, 
            authority=self.authority, 
            token_cache=self.cache
        )

    def get_token(self):
        accounts = self.app.get_accounts()
        result = None

        if accounts:
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])

        if not result:
            result = self.app.acquire_token_interactive(scopes=self.scopes, prompt="consent")
            
        if result and 'access_token' in result:
            with open(self.cache_path, "w") as f:
                f.write(self.cache.serialize())
            return result['access_token']

        return None