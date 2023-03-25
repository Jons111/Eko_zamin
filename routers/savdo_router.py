from fastapi import APIRouter, Depends, HTTPException


from db.config import Base, engine, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

from functions.savdo_functions import SavdoClass
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
#db imports
from db.config import get_db



from models.user_model import *
from schemas.basemodels import *

router_savdo = APIRouter()

@router_savdo.post('/add', )
def partner(data: SavdoCreate,db:Session = Depends(get_db)): #get_current_user : int = Depends(routers.auth_router.get_current_user)
    return SavdoClass.insert_savdo(payload=data,db=db)

@router_savdo.get('/',  status_code = 200)
def get_all_partners(db: Session = Depends(get_db)):
    return SavdoClass.get_all_savdos(db=db)

@router_savdo.get('/{id}', status_code = 200)
def get_one_partner(id:int ,db: Session = Depends(get_db)):
    return SavdoClass.find_savdo(savdo_id=id,db=db)

@router_savdo.patch('/{id}')
def update_partner(id: int, payload:SavdoBase ,db:Session=Depends(get_db)):
    return SavdoClass.update_savdo(savdo_id=id,payload=payload,db=db)