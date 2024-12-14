from celery import shared_task
import logging

from settings import config
from utils.edge_key import decode_edge_key, EdgeKey
import requests

logger = logging.getLogger('agent_logger')


@shared_task()
def send_result_backup(file_path: str, generated_id: str, result: str, method: str):
    logger.info("Starting task : Sending result backup")

    try:
        edge_key = config.EDGE_KEY
        edge_key_data, status = decode_edge_key(edge_key)

        url = f"{edge_key_data.serverUrl}/api/agent/{edge_key_data.agentId}/backup"
        logger.info(f'Status request | {url}')

        form_data = {
            "generatedId": (None, generated_id),  # Use (None, value) for non-file fields
            "status": (None, result),
            "method": (None, method),
            "file": (f"{generated_id}.dump", open(file_path, "rb"), "application/octet-stream")
        }

        print(form_data)

        response = requests.post(url=url, files=form_data)
        response.raise_for_status()
        message = response.json()
        logger.info(f'Successfully sent result backup')
        return {"message": message, "result": True}

    except Exception as e:
        message = f"Error sending result backup: {e}"
        logger.error(message)
        return {"message": message, "result": False}


@shared_task()
def send_result_restoration(generated_id: str, result: str):
    logger.info("Starting task : Sending result restoration")

    try:
        edge_key = config.EDGE_KEY
        edge_key_data, status = decode_edge_key(edge_key)

        url = f"{edge_key_data.serverUrl}/api/agent/{edge_key_data.agentId}/restore"
        logger.info(f'Status request | {url}')

        data = {
            "generatedId": generated_id,
            "status": result,
        }
        print(data)

        response = requests.post(url=url, json=data)
        response.raise_for_status()
        message = response.json()
        logger.info(f'Successfully sent result restore')
        return {"message": message, "result": True}

    except Exception as e:
        message = f"Error sending result restore: {e}"
        logger.error(message)
        return {"message": message, "result": False}