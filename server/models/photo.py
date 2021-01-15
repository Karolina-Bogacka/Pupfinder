from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Base


class Photo(Base):
    __tablename__ = "photos"
    photo_id = Column(Integer, primary_key=True, index=True)
    subject = relationship("Dog", backref="photos")
    subject_id = Column(Integer, ForeignKey("dogs.dog_id"))
    photo_url = Column(String(200), nullable=False)
