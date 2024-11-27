import logging

from celery import shared_task

from settings import config
from utils.clear_file_directory import clear_storage_file_path
from utils.postgres import PostgresDatabase

logger = logging.getLogger('agent_logger')


def get_database_instance(db_type: str):
    db_host = config.DB_HOST
    db_port = config.DB_PORT
    db_user = config.DB_USER
    db_password = config.DB_PASSWORD
    db_name = config.DB_NAME
    match db_type:
        case 'postgres':
            return PostgresDatabase(db_host, db_name, db_user, db_password, db_port)


@shared_task()
def backup(db_type: str):
    logger.info("Starting task : Backup")
    result = clear_storage_file_path()
    if result:
        database = get_database_instance(db_type)
        status, result = database.ping()
        if status:
            status, result = database.backup()
            print(status, result)
    return {"message": True}
