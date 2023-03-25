from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers.roll_router import router
from fastapi import FastAPI
from passlib.context import CryptContext

from sqlalchemy.orm import sessionmaker

from routers import *

from db.config import Base, engine, ACCESS_TOKEN_EXPIRE_MINUTES, get_db

Base.metadata.create_all(bind=engine)

from models.user_model import *

app = FastAPI(
    title="Implementing Security",
    description="Project to implement security in FastAPI",
    version="1.0.0"
)
Session = sessionmaker(bind=engine)
session = Session()



@app.get('/')
async def home():
    return {"message":"Welcome"}



app.include_router(
    auth_router.router,
    prefix='/user',
    tags=['Login'],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    router,
    prefix='/roll',
    tags=['Rollar '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    worker_router.router_worker,
    prefix='/worker',
    tags=['Hodimlar '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    buyurtma_router.router_buyurtma,
    prefix='/buyurtma',
    tags=['Buyurtmalar '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

app.include_router(
    savdo_router.router_savdo,
    prefix='/savdo',
    tags=['Tugatilgan savdolar  '],
    responses={200:{'description':'Ok'},201:{'description':'Created'},400:{'description':'Bad Request'},401:{'desription':'Unauthorized'}}
)

