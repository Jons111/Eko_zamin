from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database url
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/eko_zamin'

SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)

#Talk to db
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#class to describe our db
Base = declarative_base()

#dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()