import time

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from db.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models.user_model import SavdoModel
from schemas.basemodels import SavdoBase,SavdoCreate


class SavdoClass:

    @staticmethod
    def get_all_savdos(db: Session):
        """return a list of all savdos"""
        return db.query(SavdoModel).all()

    @staticmethod
    def find_savdo(savdo_id: int, db: Session):

        """returns a savdo that matches the id"""
        worker = db.query(SavdoModel).filter(SavdoModel.id == savdo_id).first()

        if not worker:
            raise HTTPException

        return worker

    @staticmethod
    def insert_savdo(payload: SavdoCreate, db: Session):
        """returns a new savdo"""
        record = SavdoModel(name=payload.name, number=payload.number, price=payload.price, worker_id=payload.worker_id,
                            price_type=payload.price_type,buyurtma_id=payload.buyurtma_id)
        db.add(record)
        db.commit()
        db.refresh(record)

        return record


    @staticmethod
    def update_savdo(savdo_id: int,payload:  SavdoBase, db: Session):
        note_query = db.query(SavdoModel).filter(SavdoModel.id == savdo_id)
        db_note = note_query.first()
        update_data = payload.dict()
        note_query.filter(SavdoModel.id == savdo_id).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_note)
        return db_note