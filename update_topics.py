import os
import sys
import requests
import json

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

from caretaker.core.config import load_config

def update_topics():
    try:
        config = load_config()
        if not config.github_token:
            print("❌ Error: GH_TOKEN not found in environment.")
            return

        # Topics to add
        topics = [
            "github-automation",
            "profile-optimizer",
            "ai-agents",
            "developer-tools",
            "productivity",
            "open-source"
        ]

        repo_name = "My-GitHub-CareTaker"
        url = f"https://api.github.com/repos/{config.username}/{repo_name}/topics"
        
        headers = {
            "Authorization": f"Bearer {config.github_token}",
            "Accept": "application/vnd.github.mercy-preview+json", # Required for topics
            "X-GitHub-Api-Version": "2022-11-28"
        }

        print(f"🚀 Updating topics for {config.username}/{repo_name}...")
        print(f"🏷️  Tags: {', '.join(topics)}")

        response = requests.put(url, headers=headers, json={"names": topics})

        if response.status_code == 200:
            print("✅ SUCCESS: Repository topics updated!")
            print(f"🔗 View here: https://github.com/{config.username}/{repo_name}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    update_topics()
