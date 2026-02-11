import os
import sys
import requests
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_USER = "welshDog"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("❌ Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def check_repo_exists(repo_name: str) -> Tuple[bool, dict]:
    """Check if a repository exists and return its metadata."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return True, resp.json()
    return False, {}

def check_branch_exists(repo_name: str, branch: str) -> bool:
    """Check if a specific branch exists."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/branches/{branch}"
    resp = requests.get(url, headers=HEADERS)
    return resp.status_code == 200

def verify_plan():
    print(f"🔍 Starting Verification for user: {GITHUB_USER}")
    print("==========================================")
    
    # 1. HyperCode Consolidation
    print("\n[Phase 1] HyperCode Consolidation")
    
    # 1.1 Merge HYPERcode-V2 -> HyperCode-V2.0
    check_merge_pair("HYPERcode-V2", "HyperCode-V2.0")
    
    # 1.2 Rename HtperCode-IDE -> HyperCode-IDE
    check_rename("HtperCode-IDE", "HyperCode-IDE")
    
    # 1.3 Merge HYPERCODE-IDE -> HyperCode-IDE
    check_merge_pair("HYPERCODE-IDE", "HyperCode-IDE") # Note: Dependent on 1.2 if 1.2 creates the target
    
    # 1.6 Fix welsdog typo
    check_rename("welsdog-designs-web3-shop", "welshdog-designs-web3-shop")
    
    # 1.7 Fix costellation typo
    check_rename("my-costellation-of-repos", "my-constellation-of-repos")

    # 2. AI Agents / BROski Consolidation
    print("\n[Phase 2] AI Agents Consolidation")
    target = "GitHub-Hyper-Agent-BROski"
    sources = ["GOD-Agent-Mode", "My-Hyper-Agents-Crew"]
    
    exists, _ = check_repo_exists(target)
    if exists:
        print(f"  ✅ Target '{target}' exists.")
    else:
        print(f"  ⚠️ Target '{target}' does NOT exist (will be created or error).")
        
    for source in sources:
        check_merge_pair(source, target)

    # 3. ADHD Tools Consolidation
    print("\n[Phase 3] ADHD Tools Consolidation")
    target = "-ULTIMATE-ADHD-BRAIN-ARCADE-"
    sources = ["BROski-Chores-App"]
    
    exists, _ = check_repo_exists(target)
    if exists:
        print(f"  ✅ Target '{target}' exists.")
    else:
        print(f"  ⚠️ Target '{target}' does NOT exist.")
        
    for source in sources:
        check_merge_pair(source, target)

    # 4. Archive Candidates
    print("\n[Phase 4] Archive Candidates (Check for existence)")
    candidates = [
        "START-HERE",
        "HYPER-coding-ap",
        "hyperflow-editor",
        "BROski-system",
        "HyperCodingApp"
    ]
    for repo in candidates:
        exists, meta = check_repo_exists(repo)
        if exists:
            desc = meta.get('description', 'No description')
            updated = meta.get('updated_at', 'Unknown')
            print(f"  ✅ Found '{repo}' (Last updated: {updated})")
        else:
            print(f"  ⚠️ '{repo}' NOT found (might already be deleted/renamed).")

def check_merge_pair(source: str, target: str):
    """Verify source and target for a merge operation."""
    s_exists, s_meta = check_repo_exists(source)
    t_exists, t_meta = check_repo_exists(target)
    
    if s_exists:
        print(f"  ✅ Source '{source}' exists ({s_meta.get('default_branch')} branch).")
    else:
        print(f"  ❌ Source '{source}' NOT found.")
        
    if t_exists:
        print(f"  ✅ Target '{target}' exists.")
    else:
        # Special case: Target might be the result of a rename in a previous step
        if target == "HyperCode-IDE":
             print(f"  ℹ️ Target '{target}' check skipped (depends on rename step).")
        else:
             print(f"  ❌ Target '{target}' NOT found.")

def check_rename(current: str, new: str):
    """Verify rename operation."""
    c_exists, _ = check_repo_exists(current)
    n_exists, _ = check_repo_exists(new)
    
    if c_exists:
        print(f"  ✅ Current '{current}' exists.")
    else:
        print(f"  ❌ Current '{current}' NOT found.")
        
    if n_exists:
        print(f"  ⚠️ New name '{new}' ALREADY EXISTS. Rename will FAIL.")
    else:
        print(f"  ✅ New name '{new}' is available.")

if __name__ == "__main__":
    verify_plan()
