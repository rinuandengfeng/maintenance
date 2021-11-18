from fastapi import FastAPI

from starlette.staticfiles import StaticFiles

# 创建工厂函数
from app.routers import info, admin, user


def create_app():
    app = FastAPI()

    # 导入路由,前缀设置
    app.include_router(user.router)
    app.include_router(info.router)
    app.include_router(admin.router)
    # 导入静态文件模板
    # statics = app.mount('/static', StaticFiles(directory="static"), name="static")
    # 异常捕获
    # register_exception(app)
    return app
