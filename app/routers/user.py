import os

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models import model
from app.models.database import get_db
from app.models.model import User

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {"description": "Not found"}},

)


# 注册用户
@router.post('/register')
async def reception(request: Request, wx_name: str, openid: str, wx_image: UploadFile = File(...),
                    verification: int = 1, db: Session = Depends(get_db)):
    image_name = wx_image.filename
    # 保存图片的位置
    cdir = os.path.dirname(os.path.dirname(__file__))
    cdir = os.path.join(cdir, "/static/upload/image/article/", )
    image_path = os.path.join(cdir, image_name)

    # 将图片保存到本地的位置
    pth = cdir.format(image_name)
    image = wx_image.file.read()
    with open('static/upload/image/' + image_name, 'wb') as f:
        f.write(image)
    db_user = model.User(wx_name=wx_name, wx_image=image_path, verification=verification, openid=openid)
    db.add(db_user)
    db.commit()
    return {
        "code": 200,
        "data": "注册用户成功!"
    }


# 登录
@router.post('/login')
async def login(request: Request, openid: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.openid == openid).first()
    if users:
        return {
            "code": 200,
            "data": "登陆成功!"
        }
    else:
        return {
            "code": 404,
            "data": "用户不存在"
        }
