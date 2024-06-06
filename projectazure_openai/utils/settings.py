import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    
    API_KEY = os.getenv("API_KEY")
    API_VERSION = os.getenv("API_VERSION")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    
    ASSISTANT_ID = "asst_TyVor4VfTQrVVqkD5IFuuTiI"

    
    