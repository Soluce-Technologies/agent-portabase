from enum import Enum
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class DBType(str, Enum):
    POSTGRES = "postgresql"
    # MYSQL = "mysql"
    # SQLITE = "sqlite"
    # MONGODB = "mongodb"
    # Add other DB types as needed


class Settings(BaseSettings):
    REDIS_SERVER: str
    REDIS_PORT: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EDGE_KEY: Optional[str] = None

    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    DB_TYPE: Optional[DBType] = None  # Use the enum here

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='allow')
