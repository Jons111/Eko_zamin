from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.config import Base, engine


Base.metadata.create_all(bind=engine)

from db.config import get_db
from functions.roll_functions import RollClass
from schemas.basemodels import *

router = APIRouter()


@router.post('/add', status_code=201)
def title(data: RollBase,db: Session=Depends(get_db)):
    return RollClass.insert_roll(payload=data,db=db )

@router.get('/',  status_code = 200 )
def get_all_titles(db: Session = Depends(get_db)):
    return RollClass.get_all_rolls(db=db)

@router.get('/{id}', status_code = 200)
def get_one_title(id:int ,db: Session = Depends(get_db)):
    return RollClass.find_roll(roll_id=id,db=db)

@router.patch('/{id}')
def update_title(id: int, payload:RollBase,db: Session = Depends(get_db) ):
    return RollClass.update_roll(roll_id=id,payload=payload,db=db)
