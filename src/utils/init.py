import json
import logging
import os
import uuid

from settings import config


# def init() -> bool:
#     """
#     Init functions executions on startup
#     :return: bool
#     """
#
#     result = initialize_directories()
#     if result:
#         config = generate_config()
#         if config:
#             print('Initialization succeed...')
#             return True
#
#     print('Initialization failed...')
#     return False


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

#
# def generate_config() -> bool:
#     """
#     Initialize the config file
#     :return: bool
#     """
#     file_name = f"{config.DATA_PATH}config/config.json"
#     default_content = {
#         "generatedId": f"{uuid.uuid4()}",
#     }
#     try:
#         if not os.path.exists(file_name):
#             with open(file_name, 'w') as file:
#                 json.dump(default_content, file, indent=4)
#         else:
#             with open(file_name, 'r') as file:
#                 content = json.load(file)
#         return True
#     except Exception as e:
#         print(f'An error occurred while generating the config file : {e}')
#         return False
