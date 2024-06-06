from openai import AzureOpenAI

from utils.settings import Settings

class Authenticate:
    
    def __init__(self):
        self.api_key = Settings.API_KEY
        self.api_version = Settings.API_VERSION
        self.azure_endpoint = Settings.AZURE_ENDPOINT
        
    def get_client(self):
        
        client = AzureOpenAI(
            api_key= self.api_key,
            api_version=self.api_version,
            azure_endpoint = self.azure_endpoint
            )
        
        return client
    
    
z=Authenticate()
print(z.get_client())
    