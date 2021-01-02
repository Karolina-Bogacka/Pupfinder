from tokenize import String

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from models import Base


class Photo(Base):
    photo_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("dogs.dog_id"))
    subject = relationship("Dog", back_populates="photos")
    photo_url = Column(String, nullable=False)
