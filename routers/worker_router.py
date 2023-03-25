from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from db.config import Base, engine, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import sessionmaker,Session

from routers import auth_router

Base.metadata.create_all(bind=engine)
#db imports
from db.config import get_db

from functions.worker_functions import WorkerClass
from models.user_model import *
from schemas.basemodels import *

router_worker = APIRouter()






@router_worker.post('/add', )
def worker(data: WorkerCreate,db: Session=Depends(get_db)):
    return WorkerClass.insert_worker(payload=data,db=db )


@router_worker.get('/',  status_code = 200)
def get_all_workers(db: Session = Depends(get_db)):
    return WorkerClass.get_all_workers(db=db)


@router_worker.get('/{id}', status_code = 200,)
def get_one_worker(id:int ,db: Session = Depends(get_db)):
    return WorkerClass.find_worker(worker_id=id,db=db)


@router_worker.patch('/{id}')
def update_worker(id: int, payload:WorkerBase ,db: Session = Depends(get_db)):
    return WorkerClass.update_worker(worker_id=id,payload=payload,db=db)


