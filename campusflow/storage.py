"""
Shared: JSON persistence, owned by Engineer A
"""
import json
import os

DEFAULT_PATH = "data/tickets.json"

def load_tickets(path=DEFAULT_PATH):
    """Load tickets from JSON. Handles missing file and malformed JSON."""
    if not os.path.exists(path):
        # Missing file = fresh start, not error
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Tickets file must contain a list")
            return data
    except json.JSONDecodeError as e:
        # Malformed JSON = clear error, DO NOT silently erase data
        raise ValueError(f"Malformed JSON in {path}: {e}. Data not erased; fix file or delete to start fresh.") from e

def save_tickets(tickets, path=DEFAULT_PATH):
    """Save tickets to JSON, creating data/ folder if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)