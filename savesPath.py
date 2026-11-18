import os
from dataclasses import dataclass

from gamesCatalog import get_game_name


def uuid_to_folder(uuid_hex):
    """Convert hex to bytes, reverse them, and convert back to uppercase hex."""
    uuid_bytes = bytes.fromhex(uuid_hex)
    return uuid_bytes[::-1].hex().upper()


def folder_to_uuid(folder):
    """Convert a folder name back to its original UUID format."""
    folder_bytes = bytes.fromhex(folder)
    return folder_bytes[::-1].hex()


# Get the save path(s) for a specific user based on their UUID and the nand path.
# If game_id is provided, returns the path for that specific game; otherwise,
# returns the paths for all games saved by the user.
def get_user_saves_paths(nand_path, uuid_hex, game_id=None):
    user_folder = uuid_to_folder(uuid_hex)
    saves_path = os.path.join(
        nand_path, "user", "save", "0000000000000000", user_folder
    )

    if not os.path.exists(saves_path):
        return []

    if game_id:
        # Save of a specific game.
        game_path = os.path.join(saves_path, game_id)
        return [game_path] if os.path.exists(game_path) else []

    # All games of the user.
    return [
        os.path.join(saves_path, d)
        for d in os.listdir(saves_path)
        if os.path.isdir(os.path.join(saves_path, d))
    ]


def get_user_saves_info(nand_path, uuid_hex) -> list:
    """
    Returns a list of UserSaveInfo objects for each game saved by the user.
    """
    saves = get_user_saves_paths(nand_path, uuid_hex)
    return [UserSaveInfo.from_save_path(save) for save in saves]


@dataclass
class UserSaveInfo:
    """
    Represents information about a user's save for a specific game.
    """

    game_id: str
    save_path: str
    game_name: str = "Unknown Game"  # Default value if game name is not found

    @classmethod
    def from_save_path(cls, save_path: str) -> "UserSaveInfo":
        """Creates a UserSaveInfo instance from a save path.
        args:
            save_path: The path to the game's save directory.

        return:
            An instance of UserSaveInfo.
        """
        game_id = os.path.basename(save_path)
        game_name = get_game_name(
            game_id
        )  # Get the name of the game from the gamesCatalog module.
        return cls(game_id=game_id, save_path=save_path, game_name=game_name)
