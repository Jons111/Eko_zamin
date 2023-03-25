import time
from datetime import timedelta, datetime
from typing import Optional, Union

from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, APIRouter, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')



class User(BaseModel):
    username: str
    name: Union[str, None] = None
    status: Union[bool, None] = None


def check_password_hash(password, hashed_passed):
    return pwd_context.verify(password, hashed_passed)

# authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(WorkerModel).filter(WorkerModel.username == username).first()
    if not user:
        return False
    if not check_password_hash(password=password, hashed_passed=user.hashed_password):
        return False
    return user

# create access token
def create_access_token(identity: dict, expires_delta: Optional[timedelta] = None):
    """setup expiry for your tokens"""
    new_identity = identity.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # update your your dict
    new_identity.update({'exp':expire})
    # encoded token
    encoded_jwt = jwt.encode(claims=new_identity, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# get current user
async def get_identity(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # decode the token
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        identity: str = payload.get('user_id')
        if identity is None:
            raise exception
    except JWTError:
        raise exception
    return identity

async def get_identity_active(identity_active: User = Depends(get_identity)):
    """
        This function is used to get the current user.
        It is used in the routers.py file.
    """


    if not identity_active.status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Inactive Identity  {identity_active}")
    return identity_active


@router.post('/login', response_model=Token )
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):

    user = db.query(models.user_model.WorkerModel).filter(models.user_model.WorkerModel.username==user_credentials.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid username!!!")

    if not check_password_hash(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password"
        )


    access_token = create_access_token(identity={'user_id':user.id})
    return {"access_token":access_token,"type":'Bearer'}


# @router.post('/token', response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     token = create_access_token(identity={'sub': user.id}, expires_delta=access_token_expires)
#     return {"access_token": token, "token_type": "bearer"}
# def create_access_token(data:dict):
#
#     payload= data.copy()
#     payload.update( {'exp':time.time()+ACCESS_TOKEN_EXPIRE_MINUTES}
#     )
#     token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
#     return token
#
# def verify_access_token(token:str,credentials_exceration):
#     try:
#         decode_token = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
#         id:str = decode_token.get('user_id')
#         if id is None:
#             raise credentials_exceration
#         token_data = TokenData(id=id)
#     except JWTError :
#         raise credentials_exceration
#     return token_data
#
# def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
#     credentional_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                            detail=f"User not validated{token}")
#     token = verify_access_token(token,credentional_exception)
#     print(token,"*********************")
#     user= db.query(models.user_model.WorkerModel).filter(models.user_model.WorkerModel.id==token.id).first()
#
#     return user
#
# def hash(password:str):
#     return pwd_context.hash(password)
#
#
# def verify(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)
#
# @router.post('/login', response_model=Token )
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
#
#     user = db.query(models.user_model.WorkerModel).filter(models.user_model.WorkerModel.username==user_credentials.username).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid username!!!")
#
#     if not verify(user_credentials.password,user.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password"
#         )
#
#
#     access_token = create_access_token(data={'user_id':user.id})
#     return {"access_token":access_token,"type":'Bearer'}


























