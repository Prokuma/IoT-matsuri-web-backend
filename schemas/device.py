from typing import Optional
from pydantic import BaseModel, validator

class DeviceCreateRequest(BaseModel):
    name: str

class DeviceCreateResponse(DeviceCreateRequest):
    id: str
    secret: str
    class Config:
        orm_mode = True

class Device(DeviceCreateResponse):
    connection: bool

class DeviceList(BaseModel):
    devices: list[Device]

class DeviceInformation(BaseModel):
    name: str
    token: str
    connection: bool

class DeviceStatus(BaseModel):
    status: str

class DeviceMessageRequest(BaseModel):
    message: str

class DeviceMessageResponse(DeviceMessageRequest):
    is_to_device : bool
    device_id : str

    class Config:
        orm_mode = True