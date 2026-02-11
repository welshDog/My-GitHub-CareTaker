from typing import Dict, List
from datetime import datetime, timedelta

from . import Plugin
from caretaker.core.context import CareContext

class IssuesPlugin(Plugin):
    name = "issues"

    def run(self, ctx: CareContext) -> Dict:
        repos = ctx.client.list_user_repos(ctx.owner)
        cutoff = datetime.utcnow() - timedelta(days=60)
        results: List[Dict] = []
        for r in repos:
            issues = ctx.client.list_issues(ctx.owner, r["name"], state="open")
            stale = []
            for i in issues:
                updated = i.get("updated_at") or i.get("created_at")
                try:
                    dt = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    continue
                if dt < cutoff:
                    stale.append(i)
            if stale:
                results.append({"repo": r["name"], "stale_count": len(stale)})
        return {"plugin": self.name, "repos": results}

