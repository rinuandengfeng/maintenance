from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from app.config.settings import SECRET_KEY, ALGORITHM

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class Users(BaseModel):
    username: str


class UsersInDB(Users):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 得到加密的密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 得到用户加密后的密码
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UsersInDB(**user_dict)


# 验证登录的用户
def authenicate_user(fake_db, userid: str, password: str):
    user = get_user(fake_db, userid)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 创建进入的token
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    crendentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise crendentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise crendentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise crendentials_exception
    return user


async def get_current_active_user(current_user: Users = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=404, detail='Inactice user')
    return current_user
