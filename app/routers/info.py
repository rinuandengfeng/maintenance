from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models import model
from app.models.database import get_db
from app.models.model import Machine

router = APIRouter(
    prefix='/machine',
    tags=['machine'],
    responses={404: {"description": "Not found"}},

)


@router.get("/send")
async def send(request: Request, room: int, compet_id: int, reason: str,
               user_id: int, db: Session = Depends(get_db)):
    db_machine = model.Machine(room=room, compet_id=compet_id, reason=reason, user_id=user_id)
    db.add(db_machine)
    db.commit()
    return {
        "code": 200,
        "data": "发表成功!"
    }


# 显示所有
@router.get('/show')
async def show(request: Request, db: Session = Depends(get_db)):
    all = db.query(Machine).all()
    return {
        "code": 200,
        "data": all,
    }
