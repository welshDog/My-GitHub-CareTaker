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

    def archive_repo(self, owner: str, repo: str) -> bool:
        resp = self._request("PATCH", f"/repos/{owner}/{repo}", json={"archived": True})
        return resp.status_code == 200
