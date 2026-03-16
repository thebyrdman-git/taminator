"""
Encoded UI token storage. Tokens are stored in ~/.config/taminator/ui_tokens.json
as a base64-encoded payload so they are not plaintext in the file.
Backward compatible: reads legacy plain JSON if no encoded payload is present.
"""

import base64
import json
from pathlib import Path
from typing import Any, Dict, Optional


def _default_tokens_path() -> Path:
    return Path.home() / ".config" / "taminator" / "ui_tokens.json"


def load_ui_tokens(tokens_file: Optional[Path] = None) -> Dict[str, Any]:
    """Load UI tokens from file. Supports legacy plain JSON and encoded payload format."""
    path = tokens_file or _default_tokens_path()
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            raw = json.load(f)
    except Exception:
        return {}
    if isinstance(raw, dict) and raw.get("v") == 1 and "payload" in raw:
        try:
            decoded = base64.b64decode(raw["payload"]).decode("utf-8")
            return json.loads(decoded)
        except Exception:
            return {}
    return raw if isinstance(raw, dict) else {}


def save_ui_tokens(data: Dict[str, Any], tokens_file: Optional[Path] = None, mode: int = 0o600) -> None:
    """Save UI tokens in encoded format. Creates parent dir if needed."""
    path = tokens_file or _default_tokens_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = base64.b64encode(json.dumps(data).encode("utf-8")).decode("ascii")
    with open(path, "w") as f:
        json.dump({"v": 1, "payload": payload}, f, indent=0)
    path.chmod(mode)
