import json
from pathlib import Path

def load_json(path: str) -> dict:
    file = Path(path)
    with file.open(encoding="utf-8") as f:
        return json.load(f)
