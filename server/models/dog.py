from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Dog(Base):
    __tablename__ = "dogs"

    dog_id = Column(Integer, primary_key=True, index=True)
    chip_number = Column(Integer, unique=True)
    breed = Column(String(50))
    description = Column(String(200))
    status = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.owner_id"))
    owner = relationship("Owner", backref="dogs")
