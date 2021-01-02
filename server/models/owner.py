from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship

from models import Base
from schemas.owner import OwnerStatus


class Owner(Base):
    __tablename__ = "owners"
    owner_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)

    dogs = relationship("Dog", back_populates="owner_id")

    description = Column(String, nullable=False)
    status = Column(OwnerStatus, nullable=False)
