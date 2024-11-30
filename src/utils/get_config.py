import json
import logging

from pydantic import BaseModel, ValidationError

from settings import config
from utils.format_validation import format_validation_error

logger = logging.getLogger('agent_logger')


class Config(BaseModel):
    generatedId: str


def get_config():
    """
    Get config from config.json
    """
    file_path = f"{config.DATA_PATH}config/config.json"
    try:
        data = json.load(open(file_path))
        obj = Config.model_validate(data)
        return obj
    except ValidationError as e:
        format_validation_error(e)
