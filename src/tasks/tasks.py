import logging

from celery import shared_task
from settings import config
from utils.edge_key import decode_edge_key
from utils.status_request import status_request

logger = logging.getLogger('agent_logger')


@shared_task(name="periodic.ping_server", bind=True)
def ping_server(self):
    logger.info("Starting task : Ping server")
    edge_key = config.EDGE_KEY
    if edge_key is None:
        error = "No EDGE_KEY provided in environment variables"
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

    print(server_data)

    backup.apply_async(args=(), ignore_result=True)

    return {"message": True}


@shared_task
def backup():
    logger.info("Starting task : Backup")
    print("Backing up...")
    return {"message": True}

