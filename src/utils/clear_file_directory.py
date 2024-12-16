import logging
import os
from settings import config

logger = logging.getLogger('agent_logger')


def delete_old_file(file_name, kind):
    folder = f'{config.DATA_PATH}/files/{kind}/'
    file_path = os.path.join(folder, f'{file_name}.dump')
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
        return True
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
