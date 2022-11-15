from enum import unique
from sqlalchemy import Column, String, ForeignKey, Integer, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base


class NetworkDevice(Base):
    __tablename__ = "networkdevice"

    serialnumber = Column(String, primary_key=True, unique=True, nullable=False)
    hostname = Column(String, unique=True, nullable=False)
    platform = Column(String, nullable=False)
    version = Column(String, nullable=False)
    ipaddress = Column(String, unique=True, nullable=False)
    os = Column(String, nullable=False)
    orgid = Column(Integer, ForeignKey("organization.id"))
    organization = relationship("Organization", back_populates="networkdevice")


class UserOrgLink(Base):
    __tablename__ = "user_org_link"
    userid = Column(Integer, ForeignKey("systemuser.id"), primary_key=True)
    orgid = Column(Integer, ForeignKey("organization.id"), primary_key=True)


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, index=True, primary_key=True)
    orgname = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    networkdevice = relationship("NetworkDevice", back_populates="organization")
    systemuser = relationship(
        "SystemUser",
        secondary="user_org_link",
        back_populates="organization",
    )


class SystemUser(Base):
    __tablename__ = "systemuser"

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, unique=True, default=True)
    organization = relationship(
        "Organization",
        secondary="user_org_link",
        back_populates="systemuser",
    )
