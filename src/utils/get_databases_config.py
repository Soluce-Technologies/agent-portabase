import logging
import json
from pydantic import BaseModel, ValidationError
from typing import List

from settings import config
from utils.format_validation import format_validation_error

logger = logging.getLogger('agent_logger')


class DatabaseConfig(BaseModel):  # Inherit from BaseModel for validation
    name: str
    type: str
    username: str
    password: str
    port: int
    host: str
    generatedId: str


class DatabasesConfig(BaseModel):  # This remains as a Pydantic model
    databases: List[DatabaseConfig]


def get_databases_config():
    """
    Get database config from file provide in DATABASE_CONFIG_FILE
    """

    file_path = f"{config.DATA_PATH}/config/{config.DATABASES_CONFIG_FILE}"
    try:
        data = json.load(open(file_path))
        obj = DatabasesConfig.model_validate(data)
        return obj, True
    except ValidationError as e:
        format_validation_error(e)
        return e, False


