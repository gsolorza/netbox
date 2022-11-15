from genie.testbed import load
from typing import Any
import schema
from pprint import pprint
import json


def inventory(devices: schema.GenieBase) -> str:
    inventory: list[dict[str, str]] = []
    testbed = load(devices.dict())
    testbedDevices = testbed.devices

    for deviceName in testbedDevices.keys():
        try:
            session = testbedDevices[deviceName]
            session.connect()
            cliOutput = session.parse("show version")["version"]
            hostName = cliOutput["hostname"]
            version = cliOutput["version"]
            ipAddress = devices.devices[deviceName].ip
            platform = cliOutput["chassis"]
            serialNumber = cliOutput["chassis_sn"]
            os = devices.devices[deviceName].os
            newDevice = schema.Device(
                serialNumber=serialNumber,
                hostName=hostName,
                ipAddress=ipAddress,
                platform=platform,
                version=version,
                os=os,
            ).dict()
            session.disconnect()
            del session
            inventory.append(newDevice)
        except Exception as error:
            print(error)
            continue

    jsonInventory = json.dumps(inventory)
    return jsonInventory
