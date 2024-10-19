from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    ALLOWED_HOSTS: List[str]
    SECRET_KEY: str  # openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_SERVER: str
    REDIS_PORT: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='allow')
