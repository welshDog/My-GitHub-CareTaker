from typing import Dict, List

class CareContext:
    def __init__(self, client, owner: str):
        self.client = client
        self.owner = owner

class Plugin:
    name: str = "plugin"
    def run(self, ctx: CareContext) -> Dict:
        return {}

def load_plugins() -> List[Plugin]:
    from .duplicates import DuplicatesPlugin
    from .issues import IssuesPlugin
    from .dependencies import DependenciesPlugin
    return [DuplicatesPlugin(), IssuesPlugin(), DependenciesPlugin()]

