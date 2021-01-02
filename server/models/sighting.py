from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Sighting(Base):
    sighting_id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.dog_id"))
    dog = relationship("Dog", back_populates="sightings")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
