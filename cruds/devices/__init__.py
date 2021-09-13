from db.models import Device, Message
from sqlalchemy.orm.session import Session

def get_device(db: Session, device_id: str) -> Device:
    device = db.query(Device).filter(Device.id == device_id).first()

    return device

def get_devices_from_user_id(db: Session, user_id: str) -> list[Device]:
    devices = db.query(Device).filter(Device.id == user_id)

    return devices

def create_device(db: Session, device: Device) -> Device:
    db.add(device)
    db.commit()

    return get_device(db, device.id)

def get_message(db: Session, message_id: str) -> Message:
    message = db.query(Message).filter(Message.id == message_id).first()

    return message

def get_messages_from_device_id(db: Session, device_id: str) -> list[Message]:
    messages = db.query(Message).filter(Message.device_id == device_id)

    return messages

def create_message(db: Session, message: Message) -> Message:
    db.add(message)
    db.commit()

    return get_message(db, message.id)