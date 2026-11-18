import cProfile
import pstats
import sys

import pathDetector as pd
import savesPath as sp


def main():
    is_eden_installed, eden_path = pd.try_get_eden_path()
    if not is_eden_installed:
        print("Eden emulator not found.")
        sys.exit(1)
    nand_path = pd.get_nand_path_from_eden_path(eden_path)
    if nand_path is None:
        print("NAND path not found.")
        sys.exit(1)
    user_uuid = "027f5377b9403eeed470729c433dbe84"

    # Get user saves
    saves = sp.get_user_saves_info(nand_path, user_uuid)
    for s in saves:
        print(s)


# if __name__ == "__main__":
#     main()

with cProfile.Profile() as pr:
    main()

pstats.Stats(pr).sort_stats("cumtime").print_stats(10)
