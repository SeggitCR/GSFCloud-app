import os
from dataclasses import dataclass

MAX_USERS = 8
NAME_LENGTH = 32
UUID_LENGTH = 16


@dataclass
class EdenUser:
    """
    Represents a user in the Eden system.
    """

    uuid: str
    name: str


def get_eden_users(nand_path):
    profiles_path = os.path.join(
        nand_path, "system", "save", "8000000000000010", "su", "avators", "profiles.dat"
    )

    if not os.path.exists(profiles_path):
        return []

    with open(profiles_path, "rb") as f:
        data = f.read()

    # Calculate the real entry size based on the file size and MAX_USERS.
    ENTRY_SIZE = len(data) // MAX_USERS

    users = []

    for i in range(MAX_USERS):
        base = i * ENTRY_SIZE
        entry = data[base : base + ENTRY_SIZE]

        if entry == bytes(ENTRY_SIZE):
            continue

        # Find the first non-null byte to locate the UUID.
        uuid_start = None
        for offset in range(ENTRY_SIZE):
            if entry[offset] != 0:
                uuid_start = offset
                break

        if uuid_start is None:
            continue

        uuid = entry[uuid_start : uuid_start + UUID_LENGTH]

        # Name comes after UUID + repeated UUID + timestamp (8 bytes).
        name_start = uuid_start + UUID_LENGTH + UUID_LENGTH + 8
        raw_name = entry[name_start : name_start + NAME_LENGTH]
        user_name = raw_name.split(b"\x00")[0].decode("utf-8", errors="ignore")

        if not user_name:
            continue

        users.append(EdenUser(uuid=uuid.hex(), name=user_name))

    return users


""" 
    # Example

if __name__ == "__main__":
    nand_path = "/home/sebascr/.local/share/eden/nand"
    users = get_eden_users(nand_path)

    for u in users:
        print(f"ID: {u.uuid}  ->  Name: {u.name}")

    output:
    ID: 1234567890abcdef1234567890abcdef  ->  Name: John Doe
    ID: abcdef1234567890abcdef1234567890  ->  Name: Jane Smith
"""
