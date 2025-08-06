# config.py
from dotenv import load_dotenv
import os

def config():
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path)

    return {
        "endpoint": os.getenv("COSMOS_ENDPOINT"),
        "key": os.getenv("COSMOS_KEY"),
        "database_name": os.getenv("COSMOS_DB"),
        "container_name": os.getenv("COSMOS_CONTAINER")
    }

