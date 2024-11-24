import requests


def status_request(data):
    url = f"{data["serverUrl"]}/api/agent/{data['agentId']}/status"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), True
    else:
        return f"Request failed with status code {response.status_code}", False
