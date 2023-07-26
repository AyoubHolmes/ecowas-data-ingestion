from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)

class Kpi(Base):
    __tablename__ = "kpi"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    parentId = Column(Integer)

