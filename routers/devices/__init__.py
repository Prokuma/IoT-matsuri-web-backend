from typing import List
from schemas.user import User
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from schemas.device import Device, DeviceCreateRequest, DeviceCreateResponse ,DeviceInformation, DeviceList, DeviceMessageRequest, DeviceStatus, DeviceMessageResponse
from db import get_db, models
from cruds.users import create_user, get_user_from_token, get_password_hash, get_user
from cruds.devices import get_devices_from_user_id, create_device, get_device_from_id, change_device_info, delete_device, create_message, get_messages_from_device_id
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


device_router = APIRouter()

@device_router.get("/", response_model=List[Device])
async def devices_list(db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    devices = get_devices_from_user_id(db, user.user_id)
    return devices

@device_router.post("/register", response_model=DeviceCreateResponse)
async def register(payload: DeviceCreateRequest, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    device = create_device(db, payload.name, user)
    return device

@device_router.get("/device/{deivce_id}", response_model=Device)
async def get_device(device_id: str, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    device = get_device_from_id(db, device_id, user.user_id)
    return device

@device_router.put("/device/{deivce_id}", response_model=DeviceCreateResponse)
async def rename_device(payload: DeviceCreateRequest, device_id: str, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    device = change_device_info(db, device_id, user.user_id, payload.name)
    return device

@device_router.delete("/device/{deivce_id}", response_model=str)
async def remove_device(device_id: str, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    status = delete_device(db, device_id, user.user_id)
    return status

@device_router.post("/device/{deivce_id}/messages", response_model=DeviceMessageResponse)
async def device_operation(payload: DeviceMessageRequest, device_id: str, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_user_from_token(db, cred.credentials)
    message = create_message(payload.message, db, device_id, user.user_id)
    return message

@device_router.get("/device/{deivce_id}/message", response_model=List[DeviceMessageResponse])
async def get_device(device_id: str, db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    messages = get_messages_from_device_id(db, device_id)
    return messages