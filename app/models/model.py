from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from datetime import datetime

from sqlalchemy.orm import relationship

from app.models.database import Base


# 用户表
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wx_name = Column(String(60), nullable=True)  # 微信名字
    wx_image = Column(String(200), nullable=True)  # 微信头像
    verification = Column(Integer, default=1)  # 权限
    openid = Column(String(200), nullable=False)  # 登录id


# 坏机器表
class Machine(Base):
    __tablename__ = 'machine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room = Column(Integer, nullable=False)  # 机房
    compet_id = Column(Integer, nullable=False)  # 机器
    reason = Column(String(120), nullable=False)  # 原因
    datetime = Column(DateTime, default=datetime.now())  # 提交的时间
    user_id = Column(Integer, ForeignKey("user.id"))  # 关联用户


# 管理员表
class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=True)  # 用户名
    password = Column(String(120), nullable=True)
