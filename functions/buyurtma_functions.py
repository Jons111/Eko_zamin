import time

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from db.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models.user_model import BuyurtmaModel
from schemas.basemodels import BuyurtmaBase,BuyurtmaCreate


class BuyurtmaClass:

    @staticmethod
    def get_all_buyurtmas(db: Session):
        """return a list of all buyurtmas"""
        return db.query(BuyurtmaModel).all()

    @staticmethod
    def find_buyurtma(buyurtma_id: int, db: Session):

        """returns a buyurtma that matches the id"""
        worker = db.query(BuyurtmaModel).filter(BuyurtmaModel.id == buyurtma_id).first()

        if not worker:
            raise HTTPException

        return worker

    @staticmethod
    def insert_buyurtma(payload: BuyurtmaCreate, db: Session):
        """returns a new buyurtma"""
        worker = db.query(BuyurtmaModel).filter(BuyurtmaModel.name == payload.name).first()

        if worker:
            raise HTTPException(status_code=400, detail="buyurtma already exists!")

        else:
            record = BuyurtmaModel(name=payload.name,number=payload.number,price=payload.price,worker_id=payload.worker_id)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record


    @staticmethod
    def update_buyurtma(buyurtma_id: int,payload:  BuyurtmaBase, db: Session):
        note_query = db.query(BuyurtmaModel).filter(BuyurtmaModel.id == buyurtma_id)
        db_note = note_query.first()
        update_data = payload.dict()
        note_query.filter(BuyurtmaModel.id == buyurtma_id).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_note)
        return db_note