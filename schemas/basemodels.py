from typing import Union

from pydantic import BaseModel
from typing import Optional


class RollBase(BaseModel):
    name: str
    status: Union[bool, None] = None


class WorkerBase(BaseModel):
    name: str
    roll_id: int
    phone: str


class WorkerCreate(WorkerBase):
    kpi_per: float
    username: str
    password: str

class WorkerOut(WorkerBase):
    id: int

    class Config:
        orm_mode = True


class WorkerLogin(BaseModel):
    username: str
    password: str


class BuyurtmaBase(BaseModel):
    name: str
    number: float
    price: float


class BuyurtmaCreate(BuyurtmaBase):
    worker_id: int


class BuyurtmaOut(BuyurtmaBase):
    id: int

    class Config:
        orm_mode = True


class SavdoBase(BaseModel):
    name: str
    number: float
    price: float
    price_type: str


class SavdoCreate(SavdoBase):
    worker_id: int
    buyurtma_id: int


class SavdoOut(SavdoBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[int] = None