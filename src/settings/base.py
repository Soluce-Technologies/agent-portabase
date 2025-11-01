from enum import Enum
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

class DBType(str, Enum):
    POSTGRES = "postgresql"
    MYSQL = "mysql"
    # SQLITE = "sqlite"
    # MONGODB = "mongodb"


class Settings(BaseSettings):
    REDIS_SERVER: Optional[str] = "localhost"
    REDIS_PORT: Optional[int] = 6379

    CELERY_BROKER_URL: Optional[str] = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: Optional[str] = "redis://localhost:6379/0"

    EDGE_KEY: Optional[str] = None

    DATA_PATH: Optional[str] = f"/app/src/data"
    DATABASES_CONFIG_FILE: Optional[str] = "config.json"

    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    DB_TYPE: Optional[DBType] = None

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='allow')
