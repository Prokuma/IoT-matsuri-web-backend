from fastapi import APIRouter
from schemas.device import Device, DeviceCreateRequest, DeviceInformation, DeviceList, DeviceMessageRequest, DeviceStatus

device_router = APIRouter()

@device_router.get("/", response_model=DeviceList)
async def devices_list():
    devices = DeviceList()
    return devices

@device_router.post("/register", response_model=DeviceCreateRequest)
async def register(device: Device):
    return device

@device_router.get("/device/{deivce_id}", response_model=DeviceInformation)
async def get_device(device_id: str):
    information = DeviceInformation()
    return information

@device_router.post("/device/{deivce_id}", response_model=DeviceStatus)
async def device_operation(status: DeviceStatus, device_id: str):
    status = DeviceStatus()
    return status

@device_router.delete("/device/{deivce_id}", response_model=DeviceStatus)
async def remove_device(device_id: str):
    status = DeviceStatus()
    return status
