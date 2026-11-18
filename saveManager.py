import os
import zipfile

from savesPath import get_user_saves_paths


def export_save(nand_path, uuid_hex, game_id, base_dir):
    """
    Export a game's save data to a .zip file.

    Result:  <base_dir>/<user_uuid>/<game_id>/<game_id>.zip
    The .zip contains the save files at the archive root.

    Args:
        nand_path: base path of the emulator NAND.
        uuid_hex:  user UUID (hex, non-reversed).
        game_id:   game title id (folder name).
        base_dir:  base directory where the export will be saved.

    Returns:
        Path of the created .zip, or None if the save does not exist.
    """
    paths = get_user_saves_paths(nand_path, uuid_hex, game_id)
    if not paths:
        return None

    game_path = paths[0]

    dest_dir = os.path.join(base_dir, uuid_hex, game_id)
    os.makedirs(dest_dir, exist_ok=True)

    zip_path = os.path.join(dest_dir, f"{game_id}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(game_path):
            for file in files:
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, game_path)
                zf.write(full, arcname)

    return zip_path
