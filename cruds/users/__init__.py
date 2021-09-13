from db.models import User, LoginToken
from sqlalchemy.orm.session import Session

def get_user(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    return user

def get_user_from_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    return user

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()

    return get_user(db, user.email)

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