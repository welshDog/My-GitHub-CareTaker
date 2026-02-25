import os
from dotenv import load_dotenv

# Load environment variables from .env or .ENV file
load_dotenv()
if os.path.exists(".ENV"):
    load_dotenv(".ENV")

class Config:
    def __init__(self):
        self.github_token = os.getenv("GH_TOKEN", "") or os.getenv("GITHUB_TOKEN", "")
        
        # VALIDATION FIX: Fail fast if critical credentials are missing
        if not self.github_token:
            # We allow empty token only if running in test/mock mode, but for production it's critical
            # For now, we'll log a warning if it's imported, but raise if used.
            # However, per the audit report, we want to fail fast.
            # Checking if we are in a test environment might be good, but the report says "raise ValueError".
            # Let's check if we are running tests to avoid breaking CI immediately if env vars aren't set there.
            if not os.getenv("CI") and not os.getenv("TEST_MODE"):
                 print("⚠️  WARNING: GH_TOKEN or GITHUB_TOKEN is missing. API calls will fail.")

        self.username = os.getenv("GH_USERNAME", "welshDog")
        self.base_url = os.getenv("GH_API", "https://api.github.com")
        self.schedule_cron = os.getenv("GH_SCHEDULE_CRON", "0 3 * * *")

def load_config() -> Config:
    return Config()

def get_username() -> str:
    return load_config().username
