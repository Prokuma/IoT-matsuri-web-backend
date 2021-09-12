from pydantic import BaseModel, validator

class DeviceCreateRequest(BaseModel):
    name: str

class Device(BaseModel):
    device_id: str
    device_secret: str
    name: str
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