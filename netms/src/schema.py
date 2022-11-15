from typing import Any
from pydantic import BaseModel, validator

# from ipaddress import IPv4Address


# class CiscoOSType:
#     supportedOsTypes = ["ios", "nxos", "iosxr"]


class DeviceData(BaseModel):
    ip: str
    port: int
    protocol: str
    username: str
    password: str
    os: str


class GenieBase(BaseModel):
    devices: dict[str, DeviceData]


class Device(BaseModel):
    serialNumber: str
    hostName: str
    platform: str
    version: str
    ipAddress: str
    os: str

    # @validator("osType")
    # def osTypeIsSupported(cls, osType: str):
    #     if osType not in CiscoOSType.supportedOsTypes:
    #         raise ValueError(
    #             f"Only the following OS Types are supported: {CiscoOSType.supportedOsTypes}"
    #         )
    #     return osType

    # @validator("ipAddress")
    # def validIpAddress(cls, ipAddress: str):
    #     isValid = IPv4Address(ipAddress)
    #     return ipAddress

    class Config:
        orm_mode = True
