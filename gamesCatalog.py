# URL to fetch game info
# https://fmartingr.github.io/switch-games-json/switch_id_names.json
import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path

JSON_URL = "https://raw.githubusercontent.com/blawar/titledb/master/US.en.json"
DATA_DIR = Path(__file__).parent / "data"
JSON_RAW_PATH = DATA_DIR / "switch_games_raw.json"
INDEX_PATH = DATA_DIR / "switch_games_index.json"


""" Functions to fetch and save game info JSON from the remote URL.

    Workflow:
"""


@dataclass
class GameInfoRecord:
    game_id: str
    name: str

    def __repr__(self):
        return f"GameInfoRecord(game_id='{self.game_id}', name='{self.name}')"


def fetch_game_info() -> dict:
    """Fetches the game info JSON from the remote URL."""
    with urllib.request.urlopen(JSON_URL, timeout=10) as response:
        return json.load(response)


def save_to_cache(data: dict, path: str) -> None:
    """Saves the game info JSON to a local file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_to_index(data: dict):
    """Converts the game info to an index format."""
    index = {}
    for game_info in data.values():
        index[game_info.get("id")] = game_info.get("name", "Unknown Game")
    return index


def save_index(data: dict):
    """Saves the game info index JSON to a local file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_or_update_game_info():
    """Fetches the game info from the remote URL and saves it locally."""
    try:
        data = fetch_game_info()
        save_to_cache(data, JSON_RAW_PATH)
        index_data = convert_to_index(data)
        save_to_cache(index_data, INDEX_PATH)
        print(f"Game info updated successfully at {JSON_RAW_PATH}")
    except Exception as e:
        print(f"Failed to fetch or save game info: {e}")


def load_games_info() -> dict:
    """Loads the game info JSON from the local file and returns a dict
    keyed by nsuId."""
    if not INDEX_PATH.exists():
        return {}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def get_game_name(game_id: str) -> str:
    """Returns the game name for a given game ID."""
    return load_games_info().get(game_id, "Unknown Game")


def get_games_info_by_list(games_uuid_list: list) -> list[GameInfoRecord]:
    """Returns a list of GameInfoRecord objects for a list of game IDs."""
    games_info = load_games_info()
    return [
        GameInfoRecord(game_id=game_id, name=games_info.get(game_id, "Unknown Game"))
        for game_id in games_uuid_list
    ]
