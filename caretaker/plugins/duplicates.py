from typing import Dict, List, Tuple
from difflib import SequenceMatcher

from . import Plugin
from caretaker.core.context import CareContext

def normalize(name: str) -> str:
    return ''.join(ch.lower() for ch in name if ch.isalnum())

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

class DuplicatesPlugin(Plugin):
    name = "duplicates"

    def group(self, repos: List[Dict]) -> Dict[str, List[Dict]]:
        groups: Dict[str, List[Dict]] = {}
        for r in repos:
            n = r.get("name", "")
            key = None
            for g in list(groups.keys()):
                if similar(g, n) > 0.8:
                    key = g
                    break
            key = key or n
            groups.setdefault(key, []).append(r)
        return groups

    def choose_hero(self, group: List[Dict]) -> Dict:
        return sorted(group, key=lambda x: x.get("pushed_at") or x.get("updated_at"), reverse=True)[0]

    def run(self, ctx: CareContext) -> Dict:
        repos = ctx.client.list_user_repos(ctx.owner)
        groups = self.group(repos)
        actions: List[Dict] = []
        for name, items in groups.items():
            if len(items) <= 1:
                continue
            hero = self.choose_hero(items)
            for r in items:
                if r["name"] == hero["name"]:
                    continue
                actions.append({
                    "type": "merge_suggestion",
                    "target": hero["name"],
                    "source": r["name"],
                    "suggestion": f"Import {r['name']} into {hero['name']} under archive/"
                })
        return {"plugin": self.name, "groups": groups, "actions": actions}

