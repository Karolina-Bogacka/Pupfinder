from sqlalchemy import Column, Integer, Float, String

from models import Base


class Owner(Base):
    __tablename__ = "owners"
    owner_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(200))

    description = Column(String(200))
    status = Column(String(100))
