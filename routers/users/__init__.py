from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from schemas.user import User, UserCreateRequest, UserSignInRequest
from schemas.user import UserWithToken, UserStatus
from db import get_db
from db.models import User as UserModel
from db.models import LoginToken
from cruds.users import create_user, get_password_hash, get_user
from cruds.users import create_login_token, verify_password, delete_user
import datetime

user_router = APIRouter()

@user_router.post("/signup", response_model=User)
async def signup(user: UserCreateRequest, db: Session = Depends(get_db)):
    user_db = create_user(db, UserModel(
        name = user.username,
        email = user.email,
        password_hash = get_password_hash(user.password),
        created_at = datetime.datetime.now()
    ))

    return User(
        id = user_db.id,
        username = user_db.name,
        email = user_db.email,
        created_at = user_db.created_at
    )

@user_router.post("/signin", response_model=UserWithToken)
async def signin(user: UserSignInRequest, db: Session = Depends(get_db)):
    user_db = get_user(db, user.email)

    if not verify_password(user.password, user_db.password_hash) :
        raise HTTPException(status_code=400, detail="Sign In is failed.")

    token = create_login_token(db, LoginToken(
        token = get_password_hash(str(datetime.datetime.now()) + user.email),
        user_id = user_db.id,
        expired_at = datetime.datetime.now() + datetime.timedelta(days=14)
    ))

    return UserWithToken(
        id = user_db.id,
        username = user_db.name,
        email = user_db.email,
        created_at = user_db.created_at,
        token = token.token
    )

@user_router.delete("/remove", response_model=UserStatus)
async def remove(user: UserSignInRequest, db: Session = Depends(get_db)):
    user_db = get_user(db, user.email)
    
    if not verify_password(user.password, user_db.password_hash) :
        raise HTTPException(status_code=400, detail="Removing account is failed.")

    delete_user(db, user_db.id)

    return UserStatus(
        status = "OK"
    )