import os
from dotenv import load_dotenv

# Load environment variables from .env or .ENV file
load_dotenv()
if os.path.exists(".ENV"):
    load_dotenv(".ENV")

class Config:
    def __init__(self):
        self.github_token = os.getenv("GH_TOKEN", "") or os.getenv("GITHUB_TOKEN", "")
        self.username = os.getenv("GH_USERNAME", "welshDog")
        self.base_url = os.getenv("GH_API", "https://api.github.com")
        self.schedule_cron = os.getenv("GH_SCHEDULE_CRON", "0 3 * * *")

def load_config() -> Config:
    return Config()

def get_username() -> str:
    return load_config().username
