import logging
import requests

logger = logging.getLogger('agent_logger')


def status_request(data):
    url = f"{data["serverUrl"]}/api/agent/{data['agentId']}/status"
    logger.info(f'Status request | {url}')
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), True
    else:
        return f"Request failed with status code {response.status_code}", False
