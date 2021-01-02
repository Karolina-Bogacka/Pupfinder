from pydantic import BaseModel


class Sighting(BaseModel):
    longitude: float
