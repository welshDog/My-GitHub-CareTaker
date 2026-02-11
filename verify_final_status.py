import os
import sys
from dotenv import load_dotenv
from caretaker.core.github_client import GitHubClient

# Load environment variables
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("❌ Error: GITHUB_TOKEN not found.")
    sys.exit(1)

client = GitHubClient(token=TOKEN)

def verify_status():
    print("📊 Verifying Final GitHub Status...")
    
    # 1. Count Archived Repos
    print("\n🔍 Checking Archived Repositories...")
    # Fetch all repos
    all_repos = []
    page = 1
    while True:
        resp = client._request("GET", f"/user/repos?type=all&per_page=100&page={page}")
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        all_repos.extend(data)
        page += 1
    
    archived = [r for r in all_repos if r.get("archived")]
    active = [r for r in all_repos if not r.get("archived")]
    
    print(f"   📚 Total Repos: {len(all_repos)}")
    print(f"   🗄️  Archived: {len(archived)}")
    print(f"   ✅ Active: {len(active)}")
    
    # 2. Check Key Folders
    print("\n🔍 Checking Key Folders...")
    
    # Check HyperCode-V2.0 legacy folder
    print("   checking 'legacy' in HyperCode-V2.0...")
    resp = client._request("GET", f"/repos/welshDog/HyperCode-V2.0/contents/legacy")
    if resp.status_code == 200:
        print("   ✅ Found 'legacy' folder in HyperCode-V2.0")
    else:
        print(f"   ❌ 'legacy' folder MISSING in HyperCode-V2.0 ({resp.status_code})")

    # Check GitHub-Hyper-Agent-BROski archive/agents
    print("   checking 'archive/agents' in GitHub-Hyper-Agent-BROski...")
    resp = client._request("GET", f"/repos/welshDog/GitHub-Hyper-Agent-BROski/contents/archive/agents")
    if resp.status_code == 200:
        print("   ✅ Found 'archive/agents' folder in GitHub-Hyper-Agent-BROski")
    else:
        print(f"   ❌ 'archive/agents' folder MISSING in GitHub-Hyper-Agent-BROski ({resp.status_code})")
        
    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    verify_status()
