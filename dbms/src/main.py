from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
from settings import DEFAULTUSER, DEFAULTPASSWORD
from sqlalchemy.orm import Session
from typing import Any
import models, schema, crud

models.Base.metadata.create_all(bind=engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
defaultUser = schema.SystemUserCreds(username=DEFAULTUSER, password=DEFAULTPASSWORD)
crud.createUser(defaultUser, getDb(), crud.getUserByName)


@app.get("/getAllDevices", response_model=list[schema.NetworkDevice])
async def getAllDevice(db: Session = Depends(getDb)):
    devices = crud.getAllDevices(db)
    if devices:
        return devices
    else:
        raise HTTPException(status_code=404, detail="No devices found")


@app.get("/getDevice", response_model=schema.NetworkDevice)
async def getDevice(deviceId: schema.NetworkDeviceId, db: Session = Depends(getDb)):
    device = crud.getDevice(deviceId.serialNumber, db)
    if device:
        return device
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@app.post("/createDevice", response_model=schema.Message)
async def createDevice(
    devices: list[schema.NetworkDevice], db: Session = Depends(getDb)
):
    response = crud.createDevices(devices, db)
    return response


@app.get("/userOrgQuery", response_model=list[schema.UserAllowedOrg])
async def userOrgQuery(user: schema.SystemUserBase, db: Session = Depends(getDb)):
    response = crud.userOrgQuery(user.id, db)
    return response


@app.get("/authUser", response_model=schema.Message)
async def authUser(user: schema.SystemUserCreds, db: Session = Depends(getDb)):
    response = crud.authUser(user, db)
    return response


@app.post("/createOrg", response_model=schema.Message)
async def createOrg(org: schema.OrganizationCreate, db: Session = Depends(getDb)):
    response = crud.createOrg(org, crud.getOrgByName, db)
    return response


@app.post("/allowOrg", response_model=schema.Message)
async def allowOrg(
    association: schema.UserOrgAssociation, db: Session = Depends(getDb)
):
    response = crud.allowOrg(association, db)
    return response


# @app.get("/getUser")
# async def getUser(query: schema.Role, db: Session = Depends(getDb)):
#     role: Any = (
#         db.query(models.Role).filter(models.Role.roleName == query.roleName).first()
#     )
#     return db.query(models.User).filter(models.User.roleId == role.id).all()
