from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Sighting(Base):

    __tablename__="sightings"
    sighting_id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.dog_id"))
    dog=relationship("Dog", backref="sightings")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
