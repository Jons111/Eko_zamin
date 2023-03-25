from fastapi import APIRouter, Depends, HTTPException
from db.config import Base, engine
from functions.buyurtma_functions import BuyurtmaClass
Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from db.config import get_db

from schemas.basemodels import *

router_buyurtma = APIRouter()


@router_buyurtma.post('/add', )
def buyurtmass(payload: BuyurtmaCreate, db : Session = Depends(get_db)):
    return BuyurtmaClass.insert_buyurtma(payload=payload,db=db)

@router_buyurtma.get('/',  status_code = 200)
def get_all_buyurtmas(db: Session = Depends(get_db)):
    return BuyurtmaClass.get_all_buyurtmas(db=db)

@router_buyurtma.get('/{id}', status_code = 200)
def get_one_buyurtma(id:int ,db: Session = Depends(get_db)):
    return BuyurtmaClass.find_buyurtma(buyurtma_id=id,db=db)

@router_buyurtma.patch('/{id}')
def update_buyurtma(id: int, payload:BuyurtmaBase,db: Session = Depends(get_db) ):
    return BuyurtmaClass.update_buyurtma(buyurtma_id=id,payload=payload,db=db)