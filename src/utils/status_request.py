import logging
import requests
from utils.edge_key import EdgeKey
from utils.get_databases_config import DatabaseConfig

logger = logging.getLogger('agent_logger')


def formatted_database(database: DatabaseConfig):
    return {
        "name": database.name,
        "dbms": database.type,
        "generatedId": database.generatedId,
    }


def status_request(data: EdgeKey, databases):
    try:
        url = f"{data.serverUrl}/api/agent/{data.agentId}/status"
        logger.info(f'Status request | {url}')
        databases_items = []
        for database in databases:
            databases_items.append(formatted_database(database))
        body = {
            "databases": databases_items,
        }
        response = requests.post(url=url, json=body)
        response.raise_for_status()
        return response.json(), True

    except requests.exceptions.RequestException as e:
        # Catch and log request-related exceptions
        logger.error(f"Request error: {e}")
        return f"Request error: {e}", False

    except ValueError as e:
        # Catch and log JSON decoding errors
        logger.error(f"JSON decoding error: {e}")
        return "Failed to parse JSON response", False

    except KeyError as e:
        # Catch and log missing data keys
        logger.error(f"Missing key in input data: {e}")
        return f"Invalid input data: missing key {e}", False

    except Exception as e:
        # Catch any other exceptions
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}", False
