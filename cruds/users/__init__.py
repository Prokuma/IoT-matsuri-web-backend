from db.models import User, LoginToken
from sqlalchemy.orm.session import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    return user

def get_user_from_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    return user

def get_user_from_token(db: Session, token: str) -> LoginToken:
    user = db.query(LoginToken).filter(LoginToken.token == token).first()

    return user

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()

    return get_user(db, user.email)

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    db.query(LoginToken).filter(LoginToken.user_id == user_id).delete()
    db.delete(user)
    db.commit()

def get_login_token(db: Session, token: str) -> LoginToken:
    login_token = db.query(LoginToken).filter(LoginToken.token == token).first()

    return login_token

def get_login_tokens_from_user_id(db: Session, user_id: int) -> list[LoginToken]:
    login_tokens = db.query(LoginToken).filter(LoginToken.user_id == user_id)

    return login_tokens

def create_login_token(db: Session, login_token: LoginToken) -> LoginToken:
    db.add(login_token)
    db.commit()

    return get_login_token(db, login_token.token)