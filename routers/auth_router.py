import time
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
import models
from db.config import get_db
from models.user_model import WorkerModel
from schemas.basemodels import WorkerCreate, WorkerOut, WorkerLogin, TokenData, Token

router=APIRouter()

# setups for JWT
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 10
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')

def create_access_token(data:dict):

    payload= data.copy()
    payload.update( {'exp':time.time()+ACCESS_TOKEN_EXPIRE_MINUTES}
    )
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_access_token(token:str,credentials_exceration):
    try:
        decode_token = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = decode_token.get('user_id')
        if id is None:
            raise credentials_exceration
        token_data = TokenData(id=id)
    except JWTError :
        raise credentials_exceration
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentional_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="User not validated")
    token = verify_access_token(token,credentional_exception)
    user= db.query(models.user_model.WorkerModel).filter(models.user_model.WorkerModel.id==token.id).first()

    return user

def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

@router.post('/login', response_model=Token )
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):

    user = db.query(models.user_model.WorkerModel).filter(models.user_model.WorkerModel.username==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid username!!!")

    if not verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password"
        )


    access_token = create_access_token(data={'user_id':user.id})
    return {"access_token":access_token,"type":'Bearer'}


























