from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models import model
from app.models.database import get_db
from app.models.model import Admin
from app.utils.schemes import get_password_hash, verify_password

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    responses={404: {"description": "Not found"}},
)


# 登录
@router.post('/login')
async def login(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.username == username).first()
    if user:
        user_pass = user.password
        if verify_password(password, user_pass):
            return {
                "code": 200,
                "data": "登录成功!"
            }


# 注册
@router.post('/register')
async def register(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.username == username).first()
    if not user:
        hash_pass = get_password_hash(password)
        db_admin = model.Admin(username=username, password=hash_pass)
        db.add(db_admin)
        db.commit()
        return {
            "code": 200,
            "data": "发表成功!"
        }
    else:
        return {
            "code": 405,
            "data": "用户名已经存在!"
        }
