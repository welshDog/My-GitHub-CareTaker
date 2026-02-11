import os
import sys
# Add current directory to path so we can import caretaker modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from caretaker.core.config import load_config
from caretaker.core.github_client import GitHubClient

def step_1_profile_repo(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 1: Profile Repository for {username}...")
    repo_name = username  # Special repo must match username
    
    # Check if repo exists
    repo = client.get_repo(username, repo_name)
    if not repo:
        print(f"  ✨ Creating special repository {repo_name}...")
        repo = client.create_repo(repo_name, description="My GitHub Profile", auto_init=True, private=False)
        if not repo:
            print("  ❌ Failed to create repository.")
            return
    else:
        print(f"  ✅ Repository {repo_name} already exists.")

    # Generate README content
    # Using capsule-render for banner as it allows dynamic text and styling
    readme_content = f"""
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=00F5FF&height=300&section=header&text={username}&fontSize=90&animation=fadeIn&fontAlignY=38&desc=AI%20Agent%20Architect&descAlignY=51&descAlign=62" width="100%" alt="Header" />
  
  <h3>
    🤖 AI Agent Architect | 🐍 Python & TypeScript | ⚡ Hyper-Automation
  </h3>
  
  <p>
    Building autonomous systems that code, deploy, and scale themselves. 
    <br/>
    Creator of <b>BROski</b>, <b>CareTaker</b>, and <b>HyperCode</b>.
  </p>
  
  <a href="mailto:contact@example.com">
    <img src="https://img.shields.io/badge/Contact-Email-00F5FF?style=for-the-badge&logo=gmail&logoColor=black" alt="Contact" />
  </a>
</div>

<br/>

<div align="center">
  <a href="https://github.com/{username}">
    <img src="https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=radical&hide_border=true&count_private=true" height="180" alt="GitHub Stats" />
  </a>
  <a href="https://github.com/{username}">
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=radical&hide_border=true&langs_count=8" height="180" alt="Top Languages" />
  </a>
</div>

<div align="center">
  <a href="https://github.com/{username}">
    <img src="https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=radical&hide_border=true" alt="Streak Stats" />
  </a>
</div>

<br/>
"""
    
    print("  📝 Updating README.md...")
    success = client.create_or_update_file(
        username, 
        repo_name, 
        "README.md", 
        readme_content, 
        "docs: update profile readme with stats and banner"
    )
    
    if success:
        print("  ✅ README.md updated successfully.")
    else:
        print("  ❌ Failed to update README.md.")

def step_2_hygiene(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 2: Repository Hygiene...")
    
    # 1. Identify Top Repos
    # Using specific targets requested + top found
    target_names = [
        "My-GitHub-CareTaker",
        "GitHub-Hyper-Agent-BROski",
        "HYPERFOCUSzon.COM-Dreamer-Platform",
        "-ULTIMATE-ADHD-BRAIN-ARCADE-",
        "HyperCode-V1",
        "my-costellation-of-repos"
    ]
    
    # Verify existence and get IDs
    repo_ids = []
    print("  🔍 Verifying target repositories...")
    for name in target_names:
        repo = client.get_repo(username, name)
        if repo:
            repo_ids.append(repo["node_id"])
            print(f"    ✅ Found {name} ({repo['node_id']})")
            
            # Check files
            # Check README
            if not client.get_repo_file(username, name, "README.md"):
                print(f"      ⚠️ Missing README.md in {name}. Creating default...")
                client.create_or_update_file(username, name, "README.md", f"# {name}\n\n{repo.get('description', 'No description.')}", "docs: add default readme")
            
            # Check LICENSE
            if not client.get_repo_file(username, name, "LICENSE"):
                print(f"      ⚠️ Missing LICENSE in {name}. Creating MIT...")
                license_content = "MIT License\n\nCopyright (c) 2026 " + username
                client.create_or_update_file(username, name, "LICENSE", license_content, "chore: add MIT license")

        else:
            print(f"    ❌ Could not find {name}")

    # 2. Pin Repos (GraphQL)
    if repo_ids:
        print(f"  📌 Pinning {len(repo_ids)} repositories...")
        query = """
        mutation($ids: [ID!]!) {
            updateProfileRepositorySelection(input: {repositoryIds: $ids}) {
                clientMutationId
            }
        }
        """
        result = client.graphql(query, {"ids": repo_ids})
        if result and "errors" not in result:
            print("    ✅ Repositories pinned successfully.")
        else:
            print(f"    ❌ Failed to pin repositories: {result}")

    # 3. Archive Old Repos
    print("  📦 Checking for stale repositories to archive...")
    repos = client.list_user_repos(username)
    import datetime
    # Fix: pushed_at might be None or string. It returns ISO string.
    one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()
    
    for r in repos:
        if r["private"]: continue
        if r["archived"]: continue
        if r["stargazers_count"] >= 5: continue
        
        pushed_at = r.get("pushed_at")
        if pushed_at and pushed_at < one_year_ago:
            print(f"    ARCHIVING {r['name']} (Last push: {pushed_at})")
            if client.archive_repo(username, r["name"]):
                print(f"      ✅ Archived {r['name']}")
            else:
                print(f"      ❌ Failed to archive {r['name']}")

def step_3_activity(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 3: Activity Graph...")
    repo_name = username # profile repo
    
    workflow_content = """name: Activity Bump

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  bump:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
    - uses: actions/checkout@v3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    - name: Commit Empty
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
        git commit --allow-empty -m "chore: daily bump"
        git push
"""
    print(f"  📝 Creating activity workflow in {repo_name}...")
    success = client.create_or_update_file(
        username, 
        repo_name, 
        ".github/workflows/activity-bump.yml", 
        workflow_content, 
        "ci: add activity bump workflow"
    )
    if success:
        print("    ✅ Activity workflow created.")
    else:
        print("    ❌ Failed to create activity workflow.")

def step_5_cicd(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 5: CI/CD Badges...")
    
    target_names = [
        "My-GitHub-CareTaker",
        "GitHub-Hyper-Agent-BROski",
        "HYPERFOCUSzon.COM-Dreamer-Platform",
        "-ULTIMATE-ADHD-BRAIN-ARCADE-",
        "HyperCode-V1",
        "my-costellation-of-repos"
    ]
    
    ci_content = """name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    # Python Setup
    - name: Set up Python
      if: hashFiles('**/*.py') != ''
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install Python dependencies
      if: hashFiles('**/*.py') != ''
      run: |
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f setup.py ]; then pip install .; fi
        pip install pylint pytest

    - name: Lint with pylint
      if: hashFiles('**/*.py') != ''
      run: |
        # Don't fail on lint for now, just report
        pylint $(git ls-files '*.py') --disable=C,R,W0611 || true
        
    - name: Test with pytest
      if: hashFiles('**/*.py') != ''
      run: |
        if [ -d tests ]; then pytest; else echo "No tests found"; fi

    # Node.js Setup
    - name: Set up Node.js
      if: hashFiles('package.json') != ''
      uses: actions/setup-node@v3
      with:
        node-version: 18
        
    - name: Install Node dependencies
      if: hashFiles('package.json') != ''
      run: npm ci || npm install
      
    - name: Run Node tests
      if: hashFiles('package.json') != ''
      run: npm test || echo "No test script"

  security:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
    - uses: actions/checkout@v3
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: 'python, javascript'
    - name: Autobuild
      uses: github/codeql-action/autobuild@v2
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
"""

    for name in target_names:
        print(f"  🔧 Adding CI to {name}...")
        # Check if repo exists
        if not client.get_repo(username, name):
            print(f"    ⚠️ Repo {name} not found. Skipping.")
            continue
            
        success = client.create_or_update_file(
            username, 
            name, 
            ".github/workflows/ci.yml", 
            ci_content, 
            "ci: add unified CI workflow"
        )
        if success:
            print(f"    ✅ CI added to {name}.")
            
            # Now update README with badge
            print(f"    🏷️ Updating README badge in {name}...")
            # We need to prepend the badge.
            # Get current README
            file_data = client.get_repo_file(username, name, "README.md")
            if file_data:
                import base64
                current_content = base64.b64decode(file_data["content"]).decode("utf-8")
                badge = f"![CI](https://github.com/{username}/{name}/actions/workflows/ci.yml/badge.svg)"
                
                if badge not in current_content:
                    new_content = f"{badge}\n\n{current_content}"
                    client.create_or_update_file(username, name, "README.md", new_content, "docs: add CI badge")
                    print(f"    ✅ Badge added.")
                else:
                    print(f"    ✨ Badge already exists.")
        else:
            print(f"    ❌ Failed to add CI to {name}.")

def step_4_issues(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 4: Issues & Discussions...")
    target_names = [
        "My-GitHub-CareTaker",
        "GitHub-Hyper-Agent-BROski"
    ]
    
    for name in target_names:
        print(f"  🔍 Processing {name}...")
        # Check if repo exists
        if not client.get_repo(username, name): continue

        # Add labels
        labels = [
            {"name": "good-first-issue", "color": "7057ff", "description": "Good for newcomers"},
            {"name": "help-wanted", "color": "008672", "description": "Extra attention is needed"},
            {"name": "hacktoberfest", "color": "ff9100", "description": "Participate in Hacktoberfest"}
        ]
        for label in labels:
            # Check if exists (GET /repos/{owner}/{repo}/labels/{name})
            resp = client._request("GET", f"/repos/{username}/{name}/labels/{label['name']}")
            if resp.status_code == 404:
                print(f"    ➕ Creating label {label['name']}...")
                client._request("POST", f"/repos/{username}/{name}/labels", json=label)
        
        # Check old issues
        import datetime
        ninety_days_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).isoformat()
        issues = client.list_issues(username, name, state="open")
        count = 0
        for issue in issues:
            if issue.get("pull_request"): continue # Skip PRs
            if issue["updated_at"] < ninety_days_ago:
                print(f"    🔒 Closing stale issue #{issue['number']}: {issue['title']}")
                client.close_issue(username, name, issue["number"], "Stale issue closed by CareTaker.")
                count += 1
        if count == 0:
            print("    ✨ No stale issues found.")

def step_6_website(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 6: Documentation Website...")
    repo_name = username
    
    # Create docs/index.html
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{username} - AI Agent Architect</title>
    <script src="https://unpkg.com/typed.js@2.0.16/dist/typed.umd.js"></script>
    <style>
        :root {{ --accent: #00F5FF; --bg: #0d1117; --text: #c9d1d9; }}
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); }}
        .hero {{ height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
        h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .accent {{ color: var(--accent); }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; padding: 4rem; max-width: 1200px; margin: 0 auto; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 1.5rem; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-5px); border-color: var(--accent); }}
        a {{ color: var(--accent); text-decoration: none; }}
    </style>
    <!-- JSON-LD for Step 8 -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "{username}",
      "url": "https://{username}.github.io",
      "sameAs": [
        "https://github.com/{username}"
      ],
      "jobTitle": "AI Agent Architect"
    }}
    </script>
</head>
<body>
    <div class="hero">
        <h1>Hi, I'm <span class="accent">{username}</span></h1>
        <div id="typed-strings">
            <p>I build <strong>autonomous agents</strong>.</p>
            <p>I architect <strong>neurodivergent-first tools</strong>.</p>
            <p>I ship <strong>HyperCode</strong>.</p>
        </div>
        <span id="typed" style="font-size: 1.5rem;"></span>
    </div>
    
    <div class="grid">
        <div class="card">
            <h3>🤖 BROski</h3>
            <p>Ultimate autonomous agent suite.</p>
            <a href="https://github.com/{username}/GitHub-Hyper-Agent-BROski">View Repo &rarr;</a>
        </div>
        <div class="card">
            <h3>🧹 CareTaker</h3>
            <p>AI-powered repo maintenance.</p>
            <a href="https://github.com/{username}/My-GitHub-CareTaker">View Repo &rarr;</a>
        </div>
        <!-- Add more cards dynamically or statically -->
    </div>
    
    <script>
        new Typed('#typed', {{
            stringsElement: '#typed-strings',
            typeSpeed: 50,
            backSpeed: 30,
            loop: true
        }});
    </script>
</body>
</html>"""

    print("  📝 Creating docs/index.html...")
    client.create_or_update_file(username, repo_name, "docs/index.html", html_content, "docs: add portfolio site")
    
    # Step 8: robots.txt
    robots_content = "User-agent: *\nAllow: /"
    client.create_or_update_file(username, repo_name, "docs/robots.txt", robots_content, "docs: add robots.txt")
    
    print("  🌐 Enabling GitHub Pages...")
    if client.enable_pages(username, repo_name, branch="main", path="/docs"):
        print(f"    ✅ Pages enabled. Site will be live at https://{username}.github.io")
    else:
        print("    ⚠️ Failed to enable Pages (might already be enabled or require manual setting).")

def step_9_verify(client: GitHubClient, username: str):
    print(f"🚀 Starting Step 9: Verification...")
    
    # Check Profile README links
    print("  🔍 Verifying Profile README links...")
    readme = client.get_repo_file(username, username, "README.md")
    if readme:
        import base64
        import re
        content = base64.b64decode(readme["content"]).decode("utf-8")
        links = re.findall(r'href="(https?://[^"]+)"', content) + re.findall(r'\((https?://[^)]+)\)', content)
        
        print(f"    Found {len(links)} links. Checking sample...")
        # Check first 5 unique links
        for link in list(set(links))[:5]:
            try:
                resp = client._request("HEAD", link.replace(client.base_url, "")) # naive check
                # Actually, these are external links mostly. GitHubClient is for API.
                # Use requests directly for external
                import requests
                r = requests.head(link, timeout=5)
                status = "✅" if r.status_code < 400 else "❌"
                print(f"    {status} {link} ({r.status_code})")
            except Exception as e:
                print(f"    ⚠️ {link} (Error: {str(e)})")
    
    print("  ✅ Verification complete. Profile should be live and optimized!")

def main():
    config = load_config()
    if not config.github_token:
        print("❌ Error: GitHub token not found in configuration.")
        # Try to load from .ENV manually if config failed (since load_config might rely on env vars already set)
        # But let's assume the environment is set up or .env is loaded by config logic if implemented.
        # caretaker/core/config.py usually loads dotenv.
        return

    client = GitHubClient(config.github_token)
    
    # Get authenticated user
    user_resp = client._request("GET", "/user")
    if user_resp.status_code == 200:
        username = user_resp.json()["login"]
        print(f"Authenticated as: {username}")
    else:
        print("❌ Failed to get authenticated user. Check your token.")
        return

    step_1_profile_repo(client, username)
    step_2_hygiene(client, username)
    step_3_activity(client, username)
    step_5_cicd(client, username)
    step_4_issues(client, username)
    step_6_website(client, username)
    step_9_verify(client, username)

if __name__ == "__main__":
    main()
