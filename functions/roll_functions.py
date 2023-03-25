import time

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from db.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models.user_model import RollModel
from schemas.basemodels import RollBase


class RollClass:

    @staticmethod
    def get_all_rolls(db: Session):
        """return a list of all rolls"""
        return db.query(RollModel).all()

    @staticmethod
    def find_roll(roll_id: int, db: Session):

        """returns a roll that matches the id"""
        worker = db.query(RollModel).filter(RollModel.id == roll_id).first()

        if not worker:
            raise HTTPException

        return worker

    @staticmethod
    def insert_roll(payload: RollBase, db: Session):
        """returns a new roll"""
        worker = db.query(RollModel).filter(RollModel.name == payload.name).first()

        if worker:
            raise HTTPException(status_code=400, detail="Roll already exists!")

        else:
            record = RollModel(name=payload.name)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record


    @staticmethod
    def update_roll(roll_id: int,payload:  RollBase, db: Session):
        note_query = db.query(RollModel).filter(RollModel.id == roll_id)
        db_note = note_query.first()
        update_data = payload.dict()
        note_query.filter(RollModel.id == roll_id).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_note)
        return db_note