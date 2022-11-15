from typing import Any
from pydantic import BaseModel
from enum import Enum


class MessageType(Enum):
    deviceCreated = "The following device(s) have been created"
    userNotFound = "Username not found"
    invalidCredentials = "Incorrect username or password"
    successfullLogin = "Access granted"
    userNotActive = "User is not active"
    userCreated = "The following user(s) have been created"
    alreadyExist = "The following object(s) already exist"
    organizationCreated = "The following organization have been created"
    noActionNeeded = "No Action is needed based on the provided parameters"
    deletedObject = "The following object(s) have been deleted"
    associationCreated = "The following association have been created"
    orgNotFound = "Organization not found"
    generalError = "Error details"


class NetworkDeviceId(BaseModel):
    serialNumber: str

    class Config:
        orm_mode = True


class NetworkDevice(NetworkDeviceId):
    hostName: str
    platform: str
    version: str
    ipAddress: str
    os: str
    orgid: int


class SystemUserBase(BaseModel):
    id: int


class SystemUserData(SystemUserBase):
    username: str
    active: bool = True


class SystemUserCreds(BaseModel):
    username: str
    password: str


class OrganizationBase(BaseModel):
    orgname: str


class OrganizationCreate(OrganizationBase):
    username: str
    password: str


class Organization(OrganizationBase):
    id: int


class UserAllowedOrg(BaseModel):
    username: str
    orgname: str
    id: str


class UserOrgAssociation(BaseModel):
    userid: int
    orgid: int
    allow: bool


class Message(BaseModel):
    message: dict[MessageType, list] = {}

    def add(self, messageType: MessageType, object: Any):
        if not self.message.get(messageType):
            self.message[messageType] = []

        self.message[messageType].append(object)

    class Config:
        orm_mode = True
