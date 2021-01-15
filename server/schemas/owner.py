from typing import List

from fastapi import Form
from pydantic import BaseModel

from schemas.dogschema import DogSchema


class OwnerBase(BaseModel):
    email: str
    password: str


class OwnerSchema(OwnerBase):
    owner_id: int = None
    username: str = None
    longitude: float = None
    latitude: float = None
    address: str = None
    description: str = None
    status: str = None
    dogs: List[DogSchema] = None

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
        cls,
        owner_id_: int = Form(None, alias="owner_id"),
        username: str = Form(None),
        address: str = Form(None),
        longitude: float = Form(None),
        latitude: float = Form(None),
        description: str = Form(None),
        status: str = Form(None),
        dogs: List[DogSchema] = Form(None),
    ):
        return cls(
            owner_id=owner_id_,
            username=username,
            address=address,
            longitude=longitude,
            latitude=latitude,
            description=description,
            status=status,
            dogs=dogs,
        )


class Token(BaseModel):
    access_token: str
    token_type: str
