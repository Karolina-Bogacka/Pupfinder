from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base
from schemas.dog import DogStatus


class Dog(Base):
    __tablename__ = "dogs"

    dog_id = Column(Integer, primary_key=True, index=True)
    chip_number = Column(Integer, unique=True)
    breed = Column(String)
    description = Column(String)
    status = Column(DogStatus, nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.owner_id"))

    owner = relationship("Owner", back_populates="dogs")
    photos = relationship("Photo", back_populates="dog")
    sightings = relationship("Sighting", back_populates="dog")
