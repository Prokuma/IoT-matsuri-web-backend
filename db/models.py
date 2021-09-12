from typing import Any
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
import datetime

@as_declarative()
class Base:
    id: Any
    __name__: Any
    
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=32))
    email = Column(String(length=255),unique=True)
    password_hash = Column(String)
    create_at = Column(DateTime, default=func.now())
    login_tokens = relationship('LoginToken', foreign_keys='LoginToken.user_id')
    devices = relationship('Device', foreign_keys='Device.user_id')

class LoginToken(Base):
    token = Column(String(length=255), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    expired_at = Column(DateTime, default=func.now() + datetime.timedelta(days=14))
    user = relationship('User', back_populates='login_tokens')

class Device(Base):
    id = Column(String(length=255), primary_key=True)
    secret = Column(String(length=255))
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(length=32))
    connection = Column(Boolean, default=False)
    user = relationship('User', back_populates='devices')
    messages = relationship('Message', foreign_keys='Message.device_id')

class Message(Base):
    id = Column(String(length=255), primary_key=True)
    device_id = Column(String(length=255), ForeignKey('device.id'))
    message = Column(String)
    device = relationship('Device', back_populates='messages')