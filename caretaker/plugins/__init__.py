import importlib
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from caretaker.core.context import CareContext

class Plugin:
    name: str = "plugin"
    def run(self, ctx: 'CareContext') -> Dict:
        return {}

# Registry of available plugins mapping name -> (module, class_name)
PLUGIN_REGISTRY = {
    'duplicates': ('caretaker.plugins.duplicates', 'DuplicatesPlugin'),
    'issues': ('caretaker.plugins.issues', 'IssuesPlugin'),
    'dependencies': ('caretaker.plugins.dependencies', 'DependenciesPlugin'),
    'monitor': ('caretaker.plugins.monitor', 'MonitorAgent'),
    'repo_explorer': ('caretaker.plugins.repo_explorer', 'RepoExplorerAgent'),
    'link_recovery': ('caretaker.plugins.link_recovery', 'LinkRecoveryAgent')
}

def get_plugin_class(name: str):
    """Dynamically imports and returns the plugin class"""
    if name not in PLUGIN_REGISTRY:
        return None
    
    module_name, class_name = PLUGIN_REGISTRY[name]
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        print(f"Error loading plugin {name}: {e}")
        return None

def get_plugin(name: str) -> Optional[Plugin]:
    """Instantiates a plugin by name"""
    cls = get_plugin_class(name)
    if cls:
        return cls()
    return None

def load_plugins() -> List[Plugin]:
    """Loads all registered plugins"""
    plugins = []
    for name in PLUGIN_REGISTRY:
        p = get_plugin(name)
        if p:
            plugins.append(p)
    return plugins
