from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean,Float,Text
from sqlalchemy import func
from db.config import Base


class RollModel(Base):
    __tablename__ = "rollar"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

class WorkerModel(Base):
    __tablename__ = "hodimlar"

    id = Column(Integer, primary_key=True)
    roll_id = Column(Integer, ForeignKey('rollar.id',), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    kpi_per = Column(Float, nullable=False)
    salary = Column(Float, nullable=True,default=0)
    kpi= Column(Float, nullable=True,default=0)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String, unique=True, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class BuyurtmaModel(Base):
    __tablename__ = "buyurtmalar"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    number = Column(Float, nullable=False)
    worker_id = Column(Integer, ForeignKey('hodimlar.id',),nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)






class SavdoModel(Base):
    __tablename__ = "savdolar"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price_type = Column(String, nullable=False)
    price = Column(Float,nullable=False)
    number = Column(Float,nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    worker_id = Column(Integer, ForeignKey('hodimlar.id', ondelete="CASCADE"), nullable=False)
    buyurtma_id = Column(Integer, ForeignKey('buyurtmalar.id', ondelete="CASCADE"), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)


