# coding: utf-8
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, VARCHAR, DECIMAL, FLOAT, DATETIME
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER


from src.db.session_maker import Base

metadata = Base.metadata


class Transactions(Base):
    __tablename__ = 'TRANSACTIONS'
    __table_args__ = {'schema': 'HumanActivityPredictionsDB'}

    ID = Column(VARCHAR(50), primary_key=True)
    # ID = Column(INTEGER(unsigned=True), primary_key=True, nullable=True, default=None, autoincrement=True)

    STATUS = Column(Integer)
    MESSAGE = Column(VARCHAR(50))
    CREATED_AT = Column(DATETIME)
    MODIFIED_AT = Column(DATETIME)