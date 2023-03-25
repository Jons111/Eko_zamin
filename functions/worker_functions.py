import time

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from db.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models.user_model import WorkerModel
from schemas.basemodels import WorkerCreate, WorkerBase
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


class WorkerClass:

    @staticmethod
    def get_all_workers(db: Session):
        """return a list of all workers"""
        return db.query(WorkerModel).all()

    @staticmethod
    def find_worker(worker_id: int, db: Session):

        """returns a worker that matches the id"""
        worker = db.query(WorkerModel).filter(WorkerModel.id == worker_id).first()

        if not worker:
            raise HTTPException

        return worker

    @staticmethod
    def insert_worker(payload: WorkerCreate, db: Session):
        """returns a new worker"""
        worker = db.query(WorkerModel).filter(WorkerModel.username == payload.username).first()

        if worker:
            raise HTTPException(status_code=400, detail="Worker already exists!")

        else:
            data = {"username":payload.username}
            data.update({'exp': time.time() + ACCESS_TOKEN_EXPIRE_MINUTES}
                           )
            token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            record = WorkerModel(username=payload.username, name=payload.name,phone=payload.phone,kpi_per=payload.kpi_per,
                                 roll_id=payload.roll_id,password=pwd_context.hash(payload.password,),token=token)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record


    @staticmethod
    def update_worker(worker_id: int,payload:  WorkerBase, db: Session):
        note_query = db.query(WorkerModel).filter(WorkerModel.id == worker_id)
        db_note = note_query.first()
        update_data = payload.dict()
        note_query.filter(WorkerModel.id == worker_id).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_note)
        return db_note