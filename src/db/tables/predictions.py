# coding: utf-8
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, VARCHAR, DECIMAL, FLOAT, DATETIME
from sqlalchemy.sql import func

from db.session_maker import Base

metadata = Base.metadata


class Predictions(Base):
    __tablename__ = 'PREDICTIONS'
    __table_args__ = {'schema': 'HumanActivityPredictionsDB',
                      'extend_existing': True
                      }

    ID = Column(VARCHAR(20), primary_key=True)
    TRANSACTION_ID = Column(VARCHAR(50))
    ACTIVITY_DATETIME = Column(DATETIME)
    ACTIVITY = Column(VARCHAR(30))
    RECOMMENDATION = Column(VARCHAR(100))
    CREATED_AT = Column(DATETIME)





# CREATE TABLE PREDICTIONS (
#   ID VARCHAR(20) NOT NULL,
#   TRANSACTION_ID INT,
#   ACTIVITY_DATETIME DATETIME,
#   ACTIVITY VARCHAR(30),
#   RECOMMENDATION VARCHAR(100),
#   CREATED_AT DATETIME,
#   PRIMARY KEY (id)
# );

