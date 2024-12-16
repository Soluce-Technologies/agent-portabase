import os
from settings import config


def initialize_directories() -> bool:
    """
    Initialize the directories needed to run the program.
    :return: bool
    """
    try:

        base_path = f"{config.DATA_PATH}/files"
        directories = [
            f"{base_path}/backups",
            f"{base_path}/backups/automatic",
            f"{base_path}/backups/manual",
            f"{base_path}/restorations",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        return True
    except Exception as e:
        print(f'An error occurred while initializing the directories : {e}')
        return False
