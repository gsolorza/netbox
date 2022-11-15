from pydantic import BaseModel
from genie.testbed import load
from typing import Any
from pprint import pprint
import json

devices = {
    "devices": {
        "TP-EP-RT1": {
            "ip": "10.253.8.178",
            "port": 22,
            "protocol": "ssh",
            "username": "lairdadmin",
            "password": "WgU0znN(qhxf",
            "os": "iosxe",
        },
        "TP-Bensalem-RT1": {
            "ip": "10.253.8.177",
            "port": 22,
            "protocol": "ssh",
            "username": "lairdadmin",
            "password": "WgU0znN(qhxf",
            "os": "iosxe",
        },
    }
}


class DeviceData(BaseModel):
    ip: str
    port: int
    protocol: str
    username: str
    password: str
    os: str


class GenieBase(BaseModel):
    devices: dict[str, DeviceData]


class User(BaseModel):
    userName: str
    lastName: str


data = GenieBase.parse_obj(devices)
user = User(userName="George", lastName="Solorzano")
newuser = user.json()
inventory = []
inventory.append(newuser)
pprint(json.dumps(inventory))
print(type(newuser))
# testbed = load(data.data)
# testbedDevices = testbed.devices
pprint(data.json())
