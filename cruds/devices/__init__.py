from typing import List
from db import models 
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from schemas.device import Device, DeviceList, DeviceCreateResponse, DeviceStatus, DeviceMessageResponse
from uuid import uuid4

def generate_uuid():
    return str(uuid4())

# def get_device(db: Session, device_id: str) -> Device:
#     device = db.query(Device).filter(Device.id == device_id).first()

#     return device

def get_devices_from_user_id(db: Session, user_id: str) -> List[Device]:
    db_devices = db.query(models.Device).filter(models.Device.user_id == user_id).all()
    if db_devices == None:
        raise HTTPException(400, 'UserId does not exit')
    devices=[]
    for db_device in db_devices:
        device = Device(
            id = db_device.id,
            secret = "",
            name = db_device.name,
            connection = False
        )
        devices.append(device)

    return devices

def get_device_from_id(db: Session, device_id: str, user_id: int) -> Device:
    db_device = db.query(models.Device).filter(models.Device.user_id == user_id, models.Device.id == device_id).first()
    if db_device == None:
        raise HTTPException(400, 'Device does not exit')
    
    device = Device(
        name = db_device.name,
        id = db_device.id,
        secret = db_device.secret,
        connection = False
    )

    return device

def change_device_info(db: Session, device_id: str, user_id: int, name: str) -> DeviceCreateResponse:
    device_orm = db.query(models.Device).filter(models.Device.user_id == user_id, models.Device.id == device_id).first()
    if device_orm == None:
        raise HTTPException(400, 'Device does not exit')

    device_orm.name = name

    db.commit()
    db.refresh(device_orm)
    device = DeviceCreateResponse.from_orm(device_orm)
    return device

def create_device(db: Session, name: str, user: models.LoginToken) -> DeviceCreateResponse:

    device_orm = models.Device(
        user_id = user.user_id,
        name = name,
        secret = generate_uuid()
    )

    db.add(device_orm)
    db.commit()
    db.refresh(device_orm)
    device = DeviceCreateResponse.from_orm(device_orm)
    return device

def delete_device(db: Session, device_id: str, user_id: int) -> str:
    device_orm = db.query(models.Device).filter(models.Device.user_id == user_id, models.Device.id == device_id).first()
    if device_orm == None:
        raise HTTPException(400, 'Device does not exit')
    db.delete(device_orm)
    db.commit()
    return "OK"

def get_message(db: Session, message_id: str) -> models.Message:
    message = db.query(models.Message).filter(models.Message.id == message_id).first()

    return message

def get_messages_from_device_id(db: Session, device_id: str) -> List[DeviceMessageResponse]:
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device == None:
        raise HTTPException(400, 'Device does not exit')

    db_messages = db.query(models.Message).filter(models.Message.device_id == device_id).all()
    if db_messages == []:
        raise HTTPException(400, 'Message does not exit')

    messages = []

    for db_message in db_messages:
        message = DeviceMessageResponse.from_orm(db_message)
        messages.append(message)
    return messages

def create_message(message: models.Message, db: Session, device_id: str, user_id: int) -> DeviceMessageResponse:
    db_device = db.query(models.Device).filter(models.Device.user_id == user_id, models.Device.id == device_id).first()
    if db_device == None:
        raise HTTPException(400, 'Device does not exit')

    db_message = db.query(models.Message).filter(models.Message.device_id == device_id, models.Message.message == message).first()
    if db_message != None:
        raise HTTPException(400, 'Message exit')
    
    message_orm = models.Message(
        is_to_device = False,
        device_id = device_id,
        message = message
    )

    db.add(message_orm)
    db.commit()
    db.refresh(message_orm)
    message = DeviceMessageResponse.from_orm(message_orm)
    print(message)
    return message