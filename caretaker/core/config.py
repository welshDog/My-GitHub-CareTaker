import os

def get_token():
    return os.getenv("GH_TOKEN", "")

def get_username():
    return os.getenv("GH_USERNAME", "welshDog")

def get_base_url():
    return os.getenv("GH_API", "https://api.github.com")

def get_schedule_cron():
    return os.getenv("GH_SCHEDULE_CRON", "0 3 * * *")

def load_config():
    return {
        "github_token": get_token(),
        "username": get_username(),
        "base_url": get_base_url(),
        "schedule_cron": get_schedule_cron()
    }
