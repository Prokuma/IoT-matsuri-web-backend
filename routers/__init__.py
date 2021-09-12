from fastapi import APIRouter
from .users import user_router
from .devices import device_router

router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(device_router, prefix='/devices', tags=['devices'])