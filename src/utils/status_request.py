import logging
import requests

logger = logging.getLogger('agent_logger')


def status_request(data):
    try:
        url = f"{data['serverUrl']}/api/agent/{data['agentId']}/status"
        logger.info(f'Status request | {url}')
        response = requests.get(url)
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
