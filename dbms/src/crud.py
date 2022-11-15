from typing import Any, Callable, Generator
from sqlalchemy.orm import Session
from schema import MessageType
import models, schema


def getDevice(serialNumber: str, db: Session):
    return (
        db.query(models.NetworkDevice)
        .filter(models.NetworkDevice.serialnumber == serialNumber)
        .first()
    )


def getUserByName(userName: str, db: Session):
    return (
        db.query(models.SystemUser)
        .filter(models.SystemUser.username == userName)
        .first()
    )


def getUserById(userId: int, db: Session):
    return db.query(models.SystemUser).filter(models.SystemUser.id == userId).first()


def getOrgByName(orgName: str, db: Session):
    return (
        db.query(models.Organization)
        .filter(models.Organization.orgname == orgName)
        .first()
    )


def getOrgById(orgId: int, db: Session):
    return db.query(models.Organization).filter(models.Organization.id == orgId).first()


def getAllDevices(db: Session) -> list[schema.NetworkDevice]:
    return db.query(models.NetworkDevice).all()


def authUser(user: schema.SystemUserCreds, db: Session):
    message = schema.Message()
    dbUser = (
        db.query(models.SystemUser)
        .filter(models.SystemUser.username == user.username)
        .first()
    )
    if dbUser:
        if dbUser.active:
            if dbUser.password == user.password:
                message.add(
                    MessageType.successfullLogin,
                    schema.SystemUserData(id=dbUser.id, username=dbUser.username),
                )
                return message
            else:
                message.add(MessageType.invalidCredentials, dbUser.username)
                return message
        else:
            message.add(MessageType.userNotActive, dbUser.username)
            return message
    else:
        message.add(MessageType.userNotFound, user.username)
        return message


def userOrgQuery(userId: int, db: Session) -> list[schema.UserAllowedOrg]:
    response = (
        db.query(
            models.SystemUser.username,
            models.Organization.orgname,
            models.Organization.id,
        )
        .select_from(models.UserOrgLink)
        .join(models.SystemUser)
        .filter(models.SystemUser.id == userId)
        .join(models.Organization)
        .all()
    )
    return response  # type: ignore


def createDevices(
    devices: list[schema.NetworkDevice],
    db: Session,
) -> schema.Message:

    message = schema.Message()
    for device in devices:
        if getDevice(device.serialNumber, db):
            message.add(MessageType.alreadyExist, device)
        elif getOrgById(device.orgid, db):
            try:
                newDevice = models.NetworkDevice(
                    serialnumber=device.serialNumber,
                    hostname=device.hostName,
                    platform=device.platform,
                    version=device.version,
                    ipaddress=device.ipAddress,
                    os=device.os,
                    orgid=device.orgid,
                )
                db.add(newDevice)
                db.commit()
                db.refresh(newDevice)
                message.add(MessageType.deviceCreated, device)
            except Exception as error:
                message.add(MessageType.generalError, error)
        else:
            message.add(MessageType.orgNotFound, device)
    return message


def createUser(user: schema.SystemUserCreds, session: Generator, queryUser: Callable):
    db = next(session)
    message = schema.Message()
    if queryUser(user.username, db):
        message.add(MessageType.alreadyExist, user.username)
        return message
    else:
        newUser = models.SystemUser(username=user.username, password=user.password)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        message.add(MessageType.userCreated, newUser.username)
        return message


def createOrg(org: schema.OrganizationCreate, queryOrg: Callable, db: Session):
    message = schema.Message()
    if queryOrg(org.orgname, db):
        message.add(MessageType.alreadyExist, org.orgname)
        return message
    else:
        newOrg = models.Organization(
            orgname=org.orgname, username=org.username, password=org.password
        )
        db.add(newOrg)
        db.commit()
        db.refresh(newOrg)
        query = queryOrg(org.orgname, db)
        organization = schema.Organization(id=query.id, orgname=query.orgname)
        message.add(MessageType.organizationCreated, organization)
        return message


def allowOrg(association: schema.UserOrgAssociation, db: Session):
    message = schema.Message()
    query = db.query(models.UserOrgLink).filter(
        models.UserOrgLink.userid == association.userid,
        models.UserOrgLink.orgid == association.orgid,
    )
    if association.allow and not query.first():
        newLink = models.UserOrgLink(userid=association.userid, orgid=association.orgid)
        db.add(newLink)
        db.commit()
        db.refresh(newLink)
        message.add(MessageType.associationCreated, association)
        return message
    elif not association.allow and query.first():
        query.delete()
        db.commit()
        message.add(MessageType.deletedObject, association)
        return message
    else:
        message.add(MessageType.noActionNeeded, association)
        return message
