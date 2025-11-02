import logging
from celery import shared_task
from settings import config
from utils.cron import check_and_update_cron
from utils.edge_key import decode_edge_key
from utils.get_databases_config import get_databases_config
from utils.status_request import status_request
from .database import backup, restore

logger = logging.getLogger('agent_logger')


@shared_task(name="periodic.ping_server", bind=True)
def ping_server(self):
    logger.info("Starting task : Ping server")
    edge_key = config.EDGE_KEY

    databases_config, status = get_databases_config()

    if not status:
        error = "Error while getting databases config"
        logger.error(error)
        return {"error": error}

    if edge_key is None:
        error = "No EDGE_KEY provided in environment variables"
        logger.error(error)
        return {"error": error}

    edge_key_data, status = decode_edge_key(edge_key)

    if not status:
        error = "Invalid EDGE_KEY provided in environment variables"
        logger.error(error)
        return {"error": "Invalid EDGE_KEY provided in environment variables"}

    server_data, status = status_request(edge_key_data, databases_config.databases)
    if not status:
        error = "Unable to ping server"
        logger.error(error)
        return {"error": error}

    for database in server_data['databases']:
        check_and_update_cron(database)

        if database['data']["backup"]["action"]:
            backup.apply_async(args=(database,), ignore_result=True)
        elif database['data']['restore']['action']:
            restore.apply_async(args=(database,), ignore_result=True)
        else:
            logger.info(f"No task requested for {database['generatedId']}")
    return {"message": True}
