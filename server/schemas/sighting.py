from fastapi import Form
from pydantic import BaseModel


class SightingSchema(BaseModel):
    longitude: float
    latitude: float

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
        cls, longitude: float = Form(None), latitude: float = Form(None),
    ):
        return cls(longitude=longitude, latitude=latitude)
