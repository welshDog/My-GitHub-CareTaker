import importlib
import os
import inspect
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from caretaker.core.context import CareContext

class Plugin:
    name: str = "plugin"
    def run(self, ctx: 'CareContext') -> Dict:
        return {}

# Registry of available plugins mapping name -> class
PLUGIN_REGISTRY = {}

def _discover_plugins():
    """Scans the plugins directory and populates the registry"""
    plugins_dir = os.path.dirname(__file__)
    print(f"DEBUG: Scanning plugins in {plugins_dir}")
    
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"caretaker.plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                
                # Check for 'register' function (User Requirement)
                if hasattr(module, 'register'):
                    try:
                        # Assuming register returns a Plugin instance or class
                        # But for now, let's stick to finding the class to be safe with existing code
                        pass 
                    except Exception:
                        pass
                
                # Fallback: Look for Plugin subclasses
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                        # Use the class's 'name' attribute if available, else filename
                        plugin_name = getattr(obj, 'name', filename[:-3])
                        PLUGIN_REGISTRY[plugin_name] = obj
                        print(f"DEBUG: Registered plugin {plugin_name} from {module_name}")
            except Exception as e:
                print(f"Error loading plugin {module_name}: {e}")

# Initial discovery
_discover_plugins()

def get_plugin_class(name: str):
    """Returns the plugin class from registry"""
    return PLUGIN_REGISTRY.get(name)

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
