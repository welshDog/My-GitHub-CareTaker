from typing import Optional
from caretaker.core.config import load_config
from caretaker.core.github_client import GitHubClient

class CareContext:
    def __init__(self, owner: str, client: GitHubClient, monitor=None):
        self.owner = owner
        self.client = client
        self.monitor = monitor

def build_context(owner: Optional[str] = None) -> CareContext:
    """Factory to create a fully initialized CareContext"""
    cfg = load_config()
    client = GitHubClient(cfg['github_token'], cfg['base_url'])
    
    # If owner is not provided, try to get from config
    if not owner:
        owner = cfg.get('username')
        
    return CareContext(owner=owner, client=client)
