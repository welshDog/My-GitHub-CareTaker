import os
import sys
from dotenv import load_dotenv
from caretaker.core.github_client import GitHubClient

# Load environment variables
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = "welshDog"

if not TOKEN:
    print("❌ Error: GITHUB_TOKEN not found.")
    sys.exit(1)

client = GitHubClient(token=TOKEN)
IPFS_LINK = "https://ipfs.io/ipfs/bafybeid4uhna7v7izg5623g5gnxdwznmc3hgusm7vgged3yf6rkf2ct53y"

def boost_web3_profile():
    print("🚀 Initiating Web3 Profile Upgrade...")

    # 1. Update Profile Bio
    print("\n👤 Updating GitHub Bio...")
    # Bio max length is 160 characters. Portfolio link goes to 'blog' field.
    short_bio = (
        "AI Agent Architect. Building HyperCode & BROski agents. "
        "🤓 Dyslexic thinking → Hyper vibe coding. "
        "🛠️ Carpenter turning code into neurodivergent tools."
    )
    
    # Note: 'blog' field in GitHub API corresponds to the "Website" field on profile
    if client.update_authenticated_user(bio=short_bio, blog=IPFS_LINK):
        print("   ✅ Bio and Website updated successfully.")
    else:
        print("   ⚠️ Failed to update bio/website. (Check token scope 'user' or bio length)")

    # 2. Update Repo Homepages
    print("\n🔗 Linking Repositories to IPFS Portfolio...")
    target_repos = [
        "THE-HYPERCODE",
        "My-GitHub-CareTaker",
        "GitHub-Hyper-Agent-BROski",
        "-ULTIMATE-ADHD-BRAIN-ARCADE-",
        "HyperCode-V2.0"
    ]

    for repo in target_repos:
        print(f"   → Updating homepage for {repo}...")
        if client.update_repo(GITHUB_USER, repo, homepage=IPFS_LINK):
            print("      ✅ Done.")
        else:
            print(f"      ⚠️ Failed (Repo might not exist).")

    print("\n✨ Web3 Integration Complete! You are now decentralized.")

if __name__ == "__main__":
    boost_web3_profile()
