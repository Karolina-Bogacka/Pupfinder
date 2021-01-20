import shutil
import uuid
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import models
from authentication import ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, \
    get_password_hash, create_access_token
from models import get_db
from models.dog import Dog
from models.owner import Owner
from models.photo import Photo
from models.sighting import Sighting
from schemas.dogschema import DogSchema
from schemas.owner import Token, OwnerSchema

models.Base.metadata.create_all(bind=models.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())
    owner = db.query(Owner).filter(Owner.username == form_data.username).first()
    if not owner:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, owner.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": owner.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/owners/")
async def create_owner(owner: OwnerSchema):
    db = next(get_db())
    length_owner = db.query(Owner).count()
    hashed_password = get_password_hash(owner.password)
    owner_model = Owner(
        owner_id=length_owner + 1,
        email=owner.email,
        password=hashed_password,
        username=owner.username,
    )
    db.add(owner_model)
    db.commit()
    db.refresh(owner_model)
    return {"owner": owner_model.username}


@app.get("/api/dogs/")
async def get_in_location(latitude: float, longitude: float):
    db = next(get_db())
    dogs = (
        db.query(Dog, Sighting)
        .filter(Dog.dog_id == Sighting.dog_id)
        .all()
    )
    return_dogs = [dog for dog in dogs if abs(dog[1].latitude - latitude) < 1]
    return_dogs_next = [
        dog for dog in return_dogs if abs(dog[1].longitude - longitude) < 1
    ]
    return {"dogs": return_dogs_next}


@app.get("/api/dogs/{dog_id}/photo/")
async def get_photo_of_dog(dog_id: int):
    db = next(get_db())
    photo = db.query(Photo).filter(Photo.subject_id == dog_id).first()
    if photo:
        file_like = open(photo.photo_url, mode="rb")
        return StreamingResponse(file_like, media_type="image/png")
    else:
        return ""


@app.post("/api/dogs/")
async def create_dog(dog: DogSchema):
    local = next(get_db())
    length_dog = local.query(Dog).count()
    length_sight = local.query(Sighting).count()
    length_photo = local.query(Photo).count()
    sighting = Sighting(
        sighting_id=length_sight + 1,
        dog_id=length_dog + 1,
        latitude=dog.location[0],
        longitude=dog.location[1],
    )
    dog_model = Dog(
        dog_id=length_dog + 1,
        breed=dog.breed,
        description=dog.description,
        status=dog.status,
    )
    local.add(dog_model)
    local.add(sighting)
    if dog.url:
        photo = Photo(
            photo_id=length_photo + 1, subject_id=length_dog + 1, photo_url=dog.url
        )
        local.add(photo)
        local.commit()
        local.refresh(photo)
    else:
        url = "./images/PUPFINDER.png"
        photo = Photo(
            photo_id=length_photo + 1, subject_id=length_dog + 1, photo_url=url
        )
        local.add(photo)
        local.commit()
    local.refresh(dog_model)
    local.refresh(sighting)
    return {"dog": dog_model, "sight": sighting}


@app.post("/api/photo/")
async def upload_photo(file: UploadFile = File(...)):
    new_name = "./images/" + str(uuid.uuid4()) + file.filename
    with open(new_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": new_name}
