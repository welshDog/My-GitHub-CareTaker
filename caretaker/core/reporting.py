import json
import os
from datetime import datetime
from typing import Any, Dict

def write_json(report_dir: str, name: str, data: Dict[str, Any]) -> str:
    os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(report_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat() + "Z", "data": data}, f, indent=2)
    return path

