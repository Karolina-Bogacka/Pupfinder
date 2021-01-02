from enum import Enum
from typing import List

from fastapi import Form
from pydantic import BaseModel

from schemas.photo import Photo
from schemas.sighting import Sighting


class DogStatus(Enum):
    HOMELESS = 'HOMELESS'
    SHELTERED = 'SHELTERED'
    ADOPTED = 'ADOPTED'


class Dog(BaseModel):
    dog_id: int = None
    chip_number: int = None
    sightings: List[Sighting] = []
    photos: List[Photo] = []
    breed: str = None
    description: str = None
    status: DogStatus = DogStatus.HOMELESS
    owner_id: int = None

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
            cls,
            dog_id_: int = Form(None, alias="dog_id"),
            chip_number: int = Form(None),
            sightings: List[Sighting] = Form(None),
            photos: List[Photo] = Form(None),
            breed: str = Form(None),
            description: str = Form(None),
            status: str = Form(None),
            owner_id: id = Form(None)
    ):
        return cls(
            dog_id=dog_id_,
            chip_number=chip_number,
            sightings=sightings,
            photos=photos,
            breed=breed,
            description=description,
            status=status,
            owner_id=owner_id
        )
