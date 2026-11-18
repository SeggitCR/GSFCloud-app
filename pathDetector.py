import subprocess
from pathlib import Path


# Gets the possible path where the eden emulator is installed on.
def try_get_eden_path():
    possible_paths = [
        Path("/usr/bin/eden"),
        Path("/usr/local/bin/eden"),
        Path("/usr/local/eden"),
        Path("/usr/bin/eden"),
        Path("/usr/games/eden"),
        Path(f"{Path.home()}/.local/bin/eden"),
        Path(f"{Path.home()}/.local/share/eden"),
        Path(f"{Path.home()}/.local/eden"),
        Path(f"{Path.home()}/games/eden"),
        Path(f"{Path.home()}/eden"),
    ]

    for path in possible_paths:
        if path.exists():
            return True, path
    return False, None


# Finds the qt-config.ini file in the system.
def find_qt_config_file(eden_path: Path | None = None):
    if eden_path is None:
        installed, eden_path = try_get_eden_path()
        if not installed:
            return None

    result = subprocess.run(
        ["find", str(eden_path), "-type", "f", "-path", "*/qt-config.ini"],
        check=False,
        capture_output=True,
        text=True,
    )
    paths = [p for p in result.stdout.splitlines() if p.strip()]
    return paths[0] if paths else None


# Finds the nand directory path in the qt-config.ini file.
def get_nand_path_from_qt_config(path):
    with open(path, "r") as f:
        f.read()


def get_nand_path_from_eden_path(eden_path: Path):
    """Return the NAND path based on the Eden installation path."""
    return Path.joinpath(eden_path, "nand")
