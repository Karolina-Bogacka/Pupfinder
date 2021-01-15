from fastapi import Form
from pydantic import BaseModel


class PhotoSchema(BaseModel):
    photo_id: int = None
    subject_id: int = None
    photo_url: str = None

    class Config:
        orm_mode = True

    @classmethod
    def as_form(
        cls,
        photo_id_: int = Form(None, alias="photo_id"),
        subject_id: int = Form(None),
        photo_url: str = Form(None),
    ):
        return cls(photo_id=photo_id_, subject_id=subject_id, photo_url=photo_url)
