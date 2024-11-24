import base64
import json
import logging

logger = logging.getLogger('agent_logger')


def decode_edge_key(edge_key: str):
    padding_needed = len(edge_key) % 4
    if padding_needed != 0:
        edge_key += '=' * (4 - padding_needed)
    edge_key_bytes = base64.urlsafe_b64decode(edge_key)
    edge_key_json = edge_key_bytes.decode('utf-8')
    try:
        edge_key_data = json.loads(edge_key_json)
    except Exception as error:
        error = f"An exception occurred: {str(error)}"
        logging.error(error)
        return error, False

    if 'serverUrl' in edge_key_data and 'agentId' in edge_key_data:
        return edge_key_data, True
    else:
        return "EDGE_KEY INVALID", False
