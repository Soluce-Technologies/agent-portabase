from settings import config
from utils.postgres import PostgresDatabase


def get_database_instance(db_type: str):
    db_host = config.DB_HOST
    db_port = config.DB_PORT
    db_user = config.DB_USER
    db_password = config.DB_PASSWORD
    db_name = config.DB_NAME
    match db_type:
        case 'postgresql':
            return PostgresDatabase(db_host, db_name, db_user, db_password, db_port)
