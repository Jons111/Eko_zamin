
from fastapi import APIRouter, Depends, HTTPException
from db.config import Base, engine

from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

from db.config import get_db

from functions.worker_functions import WorkerClass
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


