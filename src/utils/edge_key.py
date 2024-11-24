import base64
import json


def decode_edge_key(edge_key: str):

    padding_needed = len(edge_key) % 4
    if padding_needed != 0:
        edge_key += '=' * (4 - padding_needed)

    edge_key_bytes = base64.urlsafe_b64decode(edge_key)
    edge_key_json = edge_key_bytes.decode('utf-8')
    edge_key_data = json.loads(edge_key_json)

    if 'serverUrl' in edge_key_data and 'agentId' in edge_key_data:
        return edge_key_data, True
    else:
        return "EDGE_KEY INVALID", False
