from enum import Enum
from typing import Tuple, List

from fastapi import Form
from pydantic import BaseModel

from schemas.dog import Dog


class OwnerStatus(Enum):
    USER = 'USER'
    REGULAR = 'REGULAR'
    SHELTER = 'SHELTER'
    FOSTER = 'FOSTER'


class OwnerBase(BaseModel):
    email: str


class OwnerCreate(OwnerBase):
    password: str


class Owner(OwnerBase):
    owner_id: int = None
    longitude: float = None
    latitude: float = None
    address: str = None
    description: str = None
    status: OwnerStatus = None
    dogs: List[Dog] = None

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
            cls,
            owner_id_: int = Form(None, alias="owner_id"),
            address: str = Form(None),
            longitude: float = Form(None),
            latitude: float = Form(None),
            description: str = Form(None),
            status: OwnerStatus = Form(None),
            dogs: List[Dog] = Form(None)
    ):
        return cls(
            owner_id = owner_id_,
            address = address,
            longitude = longitude,
            latitude= latitude,
            description=description,
            status=status,
            dogs=dogs
        )
