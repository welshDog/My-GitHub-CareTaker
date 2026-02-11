import os
import sys
import shutil
import subprocess
import time
from typing import List, Optional
from dotenv import load_dotenv
from caretaker.core.github_client import GitHubClient

# Load environment variables
load_dotenv()

# Configuration
GITHUB_USER = "welshDog"
TOKEN = os.getenv("GITHUB_TOKEN")
BACKUP_DIR = os.path.join(os.getcwd(), f"github-cleanup-backup-{time.strftime('%Y%m%d')}")
WORK_DIR = os.path.join(os.getcwd(), "github-cleanup-work")

if not TOKEN:
    print("❌ Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

client = GitHubClient(token=TOKEN)

def run_command(cmd: List[str], cwd: Optional[str] = None, check: bool = True):
    """Run a shell command."""
    print(f"   $ {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Command failed: {e.stderr}")
        if check:
            raise

def git_clone(repo_name: str, cwd: str):
    """Clone a repository using HTTPS + Token."""
    if os.path.exists(os.path.join(cwd, repo_name)):
        print(f"   ℹ️  Repo {repo_name} already exists in work dir.")
        return
    
    url = f"https://{TOKEN}@github.com/{GITHUB_USER}/{repo_name}.git"
    run_command(["git", "clone", url], cwd=cwd)

def setup_work_dirs():
    """Create work and backup directories."""
    os.makedirs(WORK_DIR, exist_ok=True)
    # Note: Backup is handled by simply cloning everything fresh into WORK_DIR.
    # A true backup would involve archiving this dir.
    print(f"📁 Work directory: {WORK_DIR}")

def phase_1_hypercode():
    print("\n🔵 [Phase 1] HyperCode Consolidation")
    
    # 1.1 Merge HYPERcode-V2 -> HyperCode-V2.0
    print("   [1/7] Merging HYPERcode-V2 → HyperCode-V2.0/legacy/")
    git_clone("HyperCode-V2.0", WORK_DIR)
    git_clone("HYPERcode-V2", WORK_DIR)
    
    target_dir = os.path.join(WORK_DIR, "HyperCode-V2.0")
    source_dir = os.path.join(WORK_DIR, "HYPERcode-V2")
    
    # Configure remote and merge
    run_command(["git", "remote", "add", "dup-hypercode-v2", source_dir], cwd=target_dir, check=False)
    run_command(["git", "fetch", "dup-hypercode-v2"], cwd=target_dir)
    
    # Try merging main or master
    try:
        run_command(["git", "read-tree", "--prefix=legacy/HYPERcode-V2/", "-u", "dup-hypercode-v2/main"], cwd=target_dir)
    except:
        try:
            run_command(["git", "read-tree", "--prefix=legacy/HYPERcode-V2/", "-u", "dup-hypercode-v2/master"], cwd=target_dir)
        except:
            print("   ⚠️ Could not read tree from dup-hypercode-v2 (empty or branch mismatch).")

    run_command(["git", "commit", "-m", "chore: merge duplicate HYPERcode-V2 into legacy/\n\n- Consolidating duplicate V2 implementation\n- All code preserved in legacy/HYPERcode-V2/\n- Part of GitHub cleanup automation"], cwd=target_dir, check=False)
    run_command(["git", "push", "origin", "main"], cwd=target_dir, check=False) # Try main
    run_command(["git", "push", "origin", "master"], cwd=target_dir, check=False) # Try master
    
    # 1.2 Handle HtperCode-IDE (Merge instead of rename)
    print("   [2/7] Merging HtperCode-IDE → HyperCode-IDE/archive/ (Rename collision avoided)")
    git_clone("HyperCode-IDE", WORK_DIR)
    git_clone("HtperCode-IDE", WORK_DIR)
    
    target_dir = os.path.join(WORK_DIR, "HyperCode-IDE")
    source_dir = os.path.join(WORK_DIR, "HtperCode-IDE")
    
    run_command(["git", "remote", "add", "typo-ide", source_dir], cwd=target_dir, check=False)
    run_command(["git", "fetch", "typo-ide"], cwd=target_dir)
    
    try:
        run_command(["git", "read-tree", "--prefix=archive/HtperCode-IDE/", "-u", "typo-ide/main"], cwd=target_dir)
    except:
        try:
            run_command(["git", "read-tree", "--prefix=archive/HtperCode-IDE/", "-u", "typo-ide/master"], cwd=target_dir)
        except:
            print("   ⚠️ Could not read tree from typo-ide.")

    run_command(["git", "commit", "-m", "chore: merge typo repo HtperCode-IDE into archive/\n\n- Consolidating duplicate/typo repo\n- Part of GitHub cleanup automation"], cwd=target_dir, check=False)
    run_command(["git", "push", "origin", "main"], cwd=target_dir, check=False)
    
    # Archive HtperCode-IDE
    print("   [2b/7] Archiving HtperCode-IDE")
    client.update_repo(GITHUB_USER, "HtperCode-IDE", description="🗄️ ARCHIVED - Merged into HyperCode-IDE/archive/", archived=True)
    # Add topics requires separate call usually or replace all topics. GitHubClient update_repo sends json kwargs.
    # To add topics safely we need to get existing ones, but for now we just archive.

    # 1.3 Merge HYPERCODE-IDE -> HyperCode-IDE
    print("   [3/7] Merging HYPERCODE-IDE → HyperCode-IDE/archive/")
    git_clone("HYPERCODE-IDE", WORK_DIR)
    target_dir = os.path.join(WORK_DIR, "HyperCode-IDE")
    source_dir = os.path.join(WORK_DIR, "HYPERCODE-IDE")
    
    run_command(["git", "remote", "add", "old-ide", source_dir], cwd=target_dir, check=False)
    run_command(["git", "fetch", "old-ide"], cwd=target_dir)
    
    try:
        run_command(["git", "read-tree", "--prefix=archive/HYPERCODE-IDE/", "-u", "old-ide/main"], cwd=target_dir)
    except:
         try:
            run_command(["git", "read-tree", "--prefix=archive/HYPERCODE-IDE/", "-u", "old-ide/master"], cwd=target_dir)
         except:
             print("   ⚠️ Could not read tree from old-ide.")

    run_command(["git", "commit", "-m", "chore: consolidate HYPERCODE-IDE experiments into archive/"], cwd=target_dir, check=False)
    run_command(["git", "push", "origin", "main"], cwd=target_dir, check=False)
    
    # 1.4 Archive HYPERcode-V2
    print("   [4/7] Archiving HYPERcode-V2")
    client.update_repo(GITHUB_USER, "HYPERcode-V2", description="🗄️ ARCHIVED - Merged into HyperCode-V2.0/legacy/HYPERcode-V2", archived=True)
    
    # 1.5 Archive HYPERCODE-IDE
    print("   [5/7] Archiving HYPERCODE-IDE")
    client.update_repo(GITHUB_USER, "HYPERCODE-IDE", description="🗄️ ARCHIVED - Merged into HyperCode-IDE/archive/", archived=True)
    
    # 1.6 Fix welsdog typo
    print("   [6/7] Fixing typo: welsdog-designs-web3-shop → welshdog-designs-web3-shop")
    if client.update_repo(GITHUB_USER, "welsdog-designs-web3-shop", name="welshdog-designs-web3-shop"):
        print("      ✅ Renamed successfully.")
    else:
        print("      ⚠️ Rename failed (or already renamed).")
        
    # 1.7 Fix costellation typo
    print("   [7/7] Fixing typo: my-costellation-of-repos → my-constellation-of-repos")
    if client.update_repo(GITHUB_USER, "my-costellation-of-repos", name="my-constellation-of-repos"):
        print("      ✅ Renamed successfully.")
    else:
        print("      ⚠️ Rename failed (or already renamed).")

def phase_2_agents():
    print("\n🔵 [Phase 2] AI Agents Consolidation")
    target = "GitHub-Hyper-Agent-BROski"
    sources = ["GOD-Agent-Mode", "My-Hyper-Agents-Crew"]
    
    git_clone(target, WORK_DIR)
    target_dir = os.path.join(WORK_DIR, target)
    os.makedirs(os.path.join(target_dir, "archive", "agents"), exist_ok=True)
    # run_command(["mkdir", "-p", "archive/agents"], cwd=target_dir)
    
    for repo in sources:
        print(f"   Merging {repo}...")
        git_clone(repo, WORK_DIR)
        source_dir = os.path.join(WORK_DIR, repo)
        
        if not os.path.exists(source_dir):
            print(f"      ⚠️ Source {repo} not found locally, skipping.")
            continue
            
        run_command(["git", "remote", "add", f"agent-{repo}", source_dir], cwd=target_dir, check=False)
        run_command(["git", "fetch", f"agent-{repo}"], cwd=target_dir)
        
        try:
            run_command(["git", "read-tree", "--prefix=archive/agents/" + repo + "/", "-u", f"agent-{repo}/main"], cwd=target_dir)
        except:
            try:
                run_command(["git", "read-tree", "--prefix=archive/agents/" + repo + "/", "-u", f"agent-{repo}/master"], cwd=target_dir)
            except:
                print(f"      ⚠️ Could not merge {repo}.")
                
    run_command(["git", "commit", "-m", "chore: consolidate legacy agent repos into archive/\n\nMerged repos: " + ", ".join(sources)], cwd=target_dir, check=False)
    run_command(["git", "push", "origin", "main"], cwd=target_dir, check=False)
    
    # Archive sources
    for repo in sources:
        print(f"   Archiving {repo}...")
        client.update_repo(GITHUB_USER, repo, description=f"🗄️ ARCHIVED - Merged into {target}/archive/agents/{repo}", archived=True)

def phase_3_adhd_tools():
    print("\n🔵 [Phase 3] ADHD Tools Consolidation")
    target = "-ULTIMATE-ADHD-BRAIN-ARCADE-"
    sources = ["BROski-Chores-App"]
    
    git_clone(target, WORK_DIR)
    target_dir = os.path.join(WORK_DIR, target)
    os.makedirs(os.path.join(target_dir, "archive", "legacy-tools"), exist_ok=True)
    # run_command(["mkdir", "-p", "archive/legacy-tools"], cwd=target_dir)
    
    for repo in sources:
        print(f"   Merging {repo}...")
        git_clone(repo, WORK_DIR)
        source_dir = os.path.join(WORK_DIR, repo)
        
        if not os.path.exists(source_dir):
             continue

        run_command(["git", "remote", "add", f"tool-{repo}", source_dir], cwd=target_dir, check=False)
        run_command(["git", "fetch", f"tool-{repo}"], cwd=target_dir)
        
        try:
            run_command(["git", "read-tree", "--prefix=archive/legacy-tools/" + repo + "/", "-u", f"tool-{repo}/main"], cwd=target_dir)
        except:
            try:
                 run_command(["git", "read-tree", "--prefix=archive/legacy-tools/" + repo + "/", "-u", f"tool-{repo}/master"], cwd=target_dir)
            except:
                 print(f"      ⚠️ Could not merge {repo}.")

    run_command(["git", "commit", "-m", "chore: archive legacy ADHD tools"], cwd=target_dir, check=False)
    run_command(["git", "push", "origin", "main"], cwd=target_dir, check=False)
    
    # Archive sources
    for repo in sources:
        print(f"   Archiving {repo}...")
        client.update_repo(GITHUB_USER, repo, description=f"🗄️ ARCHIVED - Merged into {target}/archive/legacy-tools/{repo}", archived=True)

def phase_4_archive_only():
    print("\n🔵 [Phase 4] Archive Empty/Experimental Repos")
    repos = [
        "START-HERE",
        "HYPER-coding-ap",
        "hyperflow-editor",
        "BROski-system",
        "HyperCodingApp"
    ]
    for repo in repos:
        print(f"   Archiving {repo}...")
        client.update_repo(GITHUB_USER, repo, description="🗄️ ARCHIVED - Early experiment, superseded by newer implementations", archived=True)

def main():
    print(f"🚀 Starting GitHub Cleanup for {GITHUB_USER}...")
    setup_work_dirs()
    
    # phase_1_hypercode() # Already completed successfully
    phase_2_agents()
    phase_3_adhd_tools()
    phase_4_archive_only()
    
    print("\n✅ Cleanup Complete! You are now streamlined.")

if __name__ == "__main__":
    main()
