import os

from starlette.templating import Jinja2Templates

BASEAIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# templates = Jinja2Templates(directory='templates')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "123456"
# 使用的算法
ALGORITHM = "HS256"
# Token的有效时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30
