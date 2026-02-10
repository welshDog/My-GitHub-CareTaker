from typing import Dict, List, Optional

class CareContext:
    def __init__(self, client, owner: str, monitor=None):
        self.client = client
        self.owner = owner
        self.monitor = monitor

class Plugin:
    name: str = "plugin"
    def run(self, ctx: CareContext) -> Dict:
        return {}

# Re-export plugins for direct access if needed
from .duplicates import DuplicatesPlugin
from .issues import IssuesPlugin
from .dependencies import DependenciesPlugin
from .monitor import MonitorAgent
from .repo_explorer import RepoExplorerAgent
from .link_recovery import LinkRecoveryAgent

def load_plugins() -> List[Plugin]:
    return [
        DuplicatesPlugin(), 
        IssuesPlugin(), 
        DependenciesPlugin(),
        MonitorAgent(),
        RepoExplorerAgent(),
        LinkRecoveryAgent()
    ]

