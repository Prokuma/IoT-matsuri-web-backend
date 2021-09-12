from fastapi import APIRouter
from schemas.user import User, UserCreateRequest, UserSignInRequest, UserWithToken

user_router = APIRouter()

@user_router.post("/signup", response_model=User)
async def signup(user: UserCreateRequest):
    return user

@user_router.post("/signin", response_model=UserWithToken)
async def signin(user: UserSignInRequest):
    return user