import os
import sys
from dotenv import load_dotenv
from caretaker.core.github_client import GitHubClient

# Load environment variables
load_dotenv()

# Configuration
GITHUB_USER = "welshDog"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("❌ Error: GITHUB_TOKEN not found.")
    sys.exit(1)

client = GitHubClient(token=TOKEN)

def finalize_profile():
    print("🚀 Starting Final Profile Polish...")
    
    # 1. Update Descriptions
    print("\n📝 Updating Repository Descriptions...")
    
    # GitHub-Hyper-Agent-BROski
    desc_broski = "AI agent crew for GitHub automation – issues, PRs, repo management for neurodivergent devs"
    print(f"   → Updating GitHub-Hyper-Agent-BROski...")
    if client.update_repo(GITHUB_USER, "GitHub-Hyper-Agent-BROski", description=desc_broski):
        print("      ✅ Done.")
    else:
        print("      ⚠️ Failed.")

    # My-GitHub-CareTaker
    desc_caretaker = "AI-powered GitHub manager that scans repos, finds duplicates, generates cleanup scripts"
    print(f"   → Updating My-GitHub-CareTaker...")
    if client.update_repo(GITHUB_USER, "My-GitHub-CareTaker", description=desc_caretaker):
        print("      ✅ Done.")
    else:
        print("      ⚠️ Failed.")

    # 2. Add Topics
    print("\n🏷️  Adding Topics...")

    # THE-HYPERCODE
    topics_hypercode = ["hypercode", "programming-language", "neurodivergent", "adhd", "quantum-computing"]
    print(f"   → Tagging THE-HYPERCODE: {topics_hypercode}")
    if client.update_topics(GITHUB_USER, "THE-HYPERCODE", topics_hypercode):
         print("      ✅ Done.")
    else:
         print("      ⚠️ Failed (Repo might not exist or name differs).")

    # My-GitHub-CareTaker
    topics_caretaker = ["github-management", "ai-agents", "repo-cleanup", "automation", "python"]
    print(f"   → Tagging My-GitHub-CareTaker: {topics_caretaker}")
    if client.update_topics(GITHUB_USER, "My-GitHub-CareTaker", topics_caretaker):
         print("      ✅ Done.")
    else:
         print("      ⚠️ Failed.")

    print("\n✅ Final Polish Complete! Your profile is ready for pinning.")

if __name__ == "__main__":
    finalize_profile()
