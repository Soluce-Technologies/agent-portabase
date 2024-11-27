import logging
from celery import shared_task
from utils.clear_file_directory import clear_storage_file_path
from utils.get_database_instance import get_database_instance

logger = logging.getLogger('agent_logger')


@shared_task()
def backup(db_type: str):
    logger.info("Starting task : Backup")
    result = clear_storage_file_path()
    if result:
        database = get_database_instance(db_type)
        status, result = database.ping()
        if status:
            status, result, file = database.backup()

            print(status, result, file)
    return {"message": True}


@shared_task()
def restore(db_type: str):
    logger.info("Starting task : Restore")
    return {"message": True}
