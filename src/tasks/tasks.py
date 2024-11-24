from celery import shared_task
from settings import config
from utils.edge_key import decode_edge_key
from utils.status_request import status_request


@shared_task(name="periodic.ping_server", bind=True)
def ping_server(self):
    edge_key = config.EDGE_KEY
    if edge_key is None:
        return {"error": "No EDGE_KEY provided in environment variables"}

    edge_key_data, status = decode_edge_key(edge_key)

    if not status:
        return {"error": "Invalid EDGE_KEY provided in environment variables"}

    server_data, status = status_request(edge_key_data)
    if not status:
        return {"error": "Unable to ping server with provided EDGE_KEY"}
    print(server_data)
    backup.apply_async(args=(), ignore_result=True)

    return {"message": True}


@shared_task
def backup():
    print("Backing up...")
