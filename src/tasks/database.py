import logging
from celery import shared_task
from utils.clear_file_directory import delete_old_file
from utils.get_database_instance import get_database_instance
from utils.upload_restoration_file import upload_restoration_file
from .result import send_result_backup, send_result_restoration

logger = logging.getLogger('agent_logger')


@shared_task()
def backup(data):
    logger.info("Starting task : Backup")

    db_type = data['dbms']
    generated_id = data['generatedId']
    result = delete_old_file(generated_id, "backups")
    if result:
        database = get_database_instance(db_type, generated_id)
        if database:
            status, result = database.ping()
            if status:
                status, result, file = database.backup()
                if status:
                    logger.info(f"{result} : {file}")
                    logger.info("Backup task completed successfully")
                    send_result_backup.apply_async(args=(file, generated_id, "success"), ignore_result=False)
                    return {"message": True}

    send_result_backup.apply_async(args=("", generated_id, "failed"), ignore_result=True)
    logger.error("Backup task completed with error")
    return {"message": False}


@shared_task()
def restore(data):
    logger.info("Starting task : Restore")
    db_type = data['dbms']
    generated_id = data['generatedId']
    url = data['data']['restore']['file']
    result = delete_old_file(generated_id, "restorations")
    if result:
        result_upload, status = upload_restoration_file(url, generated_id)
        if status:
            database = get_database_instance(db_type, generated_id)
            if database :
                status, result = database.restore()
                if status:
                    logger.info("Restore task completed successfully")
                    send_result_restoration.apply_async(args=(generated_id, "success"), ignore_result=True)
    send_result_restoration.apply_async(args=(generated_id, "failed"), ignore_result=True)
    return {"message": False}


@shared_task()
def periodic_backup():
    print("Starting periodic backup")
    return {"message": True}
