from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    REDIS_SERVER: str
    REDIS_PORT: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EDGE_KEY: Optional[str] = None


    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='allow')
