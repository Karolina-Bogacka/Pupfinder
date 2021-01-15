from enum import Enum
from typing import List

from fastapi import Form
from pydantic import BaseModel


class DogStatus(Enum):
    HOMELESS = "HOMELESS"
    SHELTERED = "SHELTERED"
    ADOPTED = "ADOPTED"


class DogSchema(BaseModel):
    dog_id: int = None
    chip_number: str = None
    photos: List[str] = None
    location: List[float] = None
    url: str = None
    breed: str = None
    description: str = None
    status: str = None
    owner_id: int = None

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
        cls,
        dog_id_: int = Form(None, alias="dog_id"),
        chip_number: str = Form(None),
        breed: str = Form(None),
        description: str = Form(None),
        status: str = Form(None),
        owner_id: int = Form(None),
        url: str = Form(None),
    ):
        return cls(
            dog_id=dog_id_,
            chip_number=chip_number,
            breed=breed,
            description=description,
            status=status,
            owner_id=owner_id,
            url=url,
        )
