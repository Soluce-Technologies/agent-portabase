import logging

from celery import shared_task
from settings import config
from utils.edge_key import decode_edge_key
from utils.status_request import status_request
from .database import backup

logger = logging.getLogger('agent_logger')


@shared_task(name="periodic.ping_server", bind=True)
def ping_server(self):
    logger.info("Starting task : Ping server")
    edge_key = config.EDGE_KEY

    db_host = config.DB_HOST
    db_port = config.DB_PORT
    db_user = config.DB_USER
    db_password = config.DB_PASSWORD
    db_name = config.DB_NAME
    db_type = config.DB_TYPE

    if edge_key is None:
        error = "No EDGE_KEY provided in environment variables"
        logger.error(error)
        return {"error": error}

    if any(value is None for value in [db_host, db_port, db_user, db_password, db_name, db_type]):
        error = ("At least one of the database configuration values is missing [DB_HOST, DB_PORT, DB_USER, "
                 "DB_PASSWORD, DB_NAME, DB_TYPE]")
        logger.error(error)
        return {"error": error}

    edge_key_data, status = decode_edge_key(edge_key)

    if not status:
        error = "Invalid EDGE_KEY provided in environment variables"
        logger.error(error)
        return {"error": "Invalid EDGE_KEY provided in environment variables"}

    server_data, status = status_request(edge_key_data)
    if not status:
        error = "Unable to ping server with provided EDGE_KEY"
        logger.error(error)
        return {"error": error}

    if server_data['message']["backup"]["action"]:
        backup.apply_async(args=(db_type.value,), ignore_result=True)
    else:
        logger.info("No task requested")

    return {"message": True}
