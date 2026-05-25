# File: utils.py
import json
from typing import Any, Dict


def load_json_file(filepath: str) -> Any:
    """
    Load and parse JSON data from the given file path.

    Args:
        filepath: Path to the JSON file.

    Returns:
        The parsed JSON content (could be list, dict, etc.).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: Any, filepath: str) -> None:
    """
    Save Python data as formatted JSON to the given file path.

    Args:
        data: The Python data object to serialize (e.g., list or dict).
        filepath: Path where the JSON file will be written.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
