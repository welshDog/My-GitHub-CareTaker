import time
from typing import Any, Dict, List, Optional
import requests

class GitHubClient:
    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Accept": "application/vnd.github+json"})

    def _handle_rate(self, resp: requests.Response):
        remaining = int(resp.headers.get("X-RateLimit-Remaining", "1"))
        reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
        if remaining <= 1:
            now = int(time.time())
            delay = max(reset - now, 1)
            time.sleep(delay)

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        for attempt in range(3):
            resp = self.session.request(method, url, params=params, json=json, timeout=30)
            self._handle_rate(resp)
            if resp.status_code in (200, 201, 202, 204):
                return resp
            if resp.status_code in (429, 503):
                time.sleep(2 ** attempt)
                continue
            if resp.status_code == 403 and "rate limit" in resp.text.lower():
                time.sleep(10)
                continue
            break
        return resp

    def paginate(self, path: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        page = 1
        while True:
            p = dict(params or {})
            p.update({"per_page": 100, "page": page})
            resp = self._request("GET", path, params=p)
            if resp.status_code != 200:
                break
            batch = resp.json()
            if not batch:
                break
            items.extend(batch)
            page += 1
        return items

    def list_user_repos(self, username: str) -> List[Dict[str, Any]]:
        return self.paginate(f"/users/{username}/repos")

    def list_issues(self, owner: str, repo: str, state: str = "open") -> List[Dict[str, Any]]:
        return self.paginate(f"/repos/{owner}/{repo}/issues", params={"state": state})

    def create_issue(self, owner: str, repo: str, title: str, body: str) -> Dict[str, Any]:
        resp = self._request("POST", f"/repos/{owner}/{repo}/issues", json={"title": title, "body": body})
        return resp.json()

    def close_issue(self, owner: str, repo: str, issue_number: int, comment: Optional[str] = None) -> bool:
        if comment:
            self._request("POST", f"/repos/{owner}/{repo}/issues/{issue_number}/comments", json={"body": comment})
        resp = self._request("PATCH", f"/repos/{owner}/{repo}/issues/{issue_number}", json={"state": "closed"})
        return resp.status_code == 200

    def get_repo_file(self, owner: str, repo: str, path: str, ref: Optional[str] = None) -> Optional[Dict[str, Any]]:
        params = {"ref": ref} if ref else None
        resp = self._request("GET", f"/repos/{owner}/{repo}/contents/{path}", params=params)
        if resp.status_code == 200:
            return resp.json()
        return None

    def get_default_branch(self, owner: str, repo: str) -> Optional[str]:
        resp = self._request("GET", f"/repos/{owner}/{repo}")
        if resp.status_code == 200:
            return resp.json().get("default_branch")
        return None

    def get_repo(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        resp = self._request("GET", f"/repos/{owner}/{repo}")
        if resp.status_code == 200:
            return resp.json()
        return None

    def update_repo(self, owner: str, repo: str, **kwargs) -> bool:
        resp = self._request("PATCH", f"/repos/{owner}/{repo}", json=kwargs)
        return resp.status_code == 200

    def update_topics(self, owner: str, repo: str, topics: List[str]) -> bool:
        """Replace all topics for a repository."""
        # GitHub API expects {"names": ["topic1", "topic2"]}
        resp = self._request("PUT", f"/repos/{owner}/{repo}/topics", json={"names": topics})
        return resp.status_code == 200

    def update_authenticated_user(self, **kwargs) -> bool:
        """Update the authenticated user's profile (bio, blog, etc.)."""
        resp = self._request("PATCH", "/user", json=kwargs)
        return resp.status_code == 200

    def archive_repo(self, owner: str, repo: str) -> bool:
        return self.update_repo(owner, repo, archived=True)

    def create_repo(self, name: str, **kwargs) -> Optional[Dict[str, Any]]:
        resp = self._request("POST", "/user/repos", json={"name": name, **kwargs})
        if resp.status_code in (200, 201):
            return resp.json()
        return None

    def create_or_update_file(self, owner: str, repo: str, path: str, content: str, message: str, branch: str = "main") -> bool:
        import base64
        # Check if file exists to get sha
        current_file = self.get_repo_file(owner, repo, path, ref=branch)
        sha = current_file["sha"] if current_file else None
        
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        data = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }
        if sha:
            data["sha"] = sha
            
        resp = self._request("PUT", f"/repos/{owner}/{repo}/contents/{path}", json=data)
        return resp.status_code in (200, 201)

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        resp = self._request("POST", "/graphql", json={"query": query, "variables": variables or {}})
        if resp.status_code == 200:
            return resp.json()
        return None

    def enable_pages(self, owner: str, repo: str, branch: str = "main", path: str = "/") -> bool:
        # Check if already enabled
        resp = self._request("GET", f"/repos/{owner}/{repo}/pages")
        if resp.status_code == 200:
            return True
            
        headers = {"Accept": "application/vnd.github.switcheroo-preview+json"}
        data = {
            "source": {
                "branch": branch,
                "path": path
            }
        }
        resp = self._request("POST", f"/repos/{owner}/{repo}/pages", json=data) # Header might not be needed anymore, but safe to keep or try standard
        return resp.status_code in (200, 201)
