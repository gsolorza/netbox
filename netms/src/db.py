from requests import request
import json
import schema

DATABASESERVER = "127.0.0.1"
DATABASEPORT = "8000"


def create(devices: str):
    headers = {"Content-Type": "application/json"}
    url = f"http://{DATABASESERVER}:{DATABASEPORT}/createDevice"
    response = request("POST", url, headers=headers, data=devices, verify=False)
    return response.json()
