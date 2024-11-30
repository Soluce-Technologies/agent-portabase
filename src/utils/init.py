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
        file_path = f"{config.DATA_PATH}/files"
        if not os.path.exists(file_path):
            os.makedirs(file_path)

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
