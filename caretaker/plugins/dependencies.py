from typing import Dict, List

from . import Plugin
from caretaker.core.context import CareContext

class DependenciesPlugin(Plugin):
    name = "dependencies"

    def run(self, ctx: CareContext) -> Dict:
        repos = ctx.client.list_user_repos(ctx.owner)
        alerts: List[Dict] = []
        for r in repos:
            default = ctx.client.get_default_branch(ctx.owner, r["name"]) or r.get("default_branch") or "main"
            has_req = ctx.client.get_repo_file(ctx.owner, r["name"], "requirements.txt", ref=default) is not None
            has_pkg = ctx.client.get_repo_file(ctx.owner, r["name"], "package.json", ref=default) is not None
            if has_req or has_pkg:
                alerts.append({"repo": r["name"], "python": has_req, "node": has_pkg})
        return {"plugin": self.name, "repos": alerts}

