from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

from models import Base
from schemas.owner import OwnerStatus


class Owner(Base):
    __tablename__ = "owners"
    owner_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(200))

    description = Column(String(200), nullable=False)
    status = Column(String(100), nullable=False)
