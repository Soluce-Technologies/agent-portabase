import logging
import os
from functools import lru_cache

from pydantic import ValidationError

from settings.development import DevSettings
from settings.production import ProdSettings
from utils.format_validation import format_validation_error

logger = logging.getLogger('agent_logger')



@lru_cache
def get_settings():
    try:
        if os.getenv("ENVIRONMENT") == "development":
            return DevSettings()
        else:
            return ProdSettings()
    except ValidationError as e:
        format_validation_error(e)


config = get_settings()
