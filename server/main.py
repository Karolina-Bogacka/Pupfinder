from fastapi import FastAPI, Request, UploadFile, File
import shutil
import uuid
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import models
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
from models.dog import Dog
from models.photo import Photo
from models.sighting import Sighting
from schemas.dogschema import DogSchema

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


def get_db():
    try:
        yield models.db
    finally:
        models.db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("main-map.html", {"request": request, "id": id})


@app.get("/api/dogs/")
async def get_in_location(latitude: float, longitude: float):
    db = next(get_db())
    dogs = db.query(Dog, Sighting).filter(Dog.dog_id == Sighting.dog_id).all()
    return_dogs = [dog for dog in dogs if abs(dog[1].latitude - latitude) < 1]
    return_dogs_next = [dog for dog in return_dogs if abs(dog[1].longitude - longitude) < 1]
    return {"dogs": return_dogs_next}


@app.get("/api/dogs/photo/{dog_id}")
async def get_photo_of_dog(dog_id: int):
    pass


@app.post("/api/dogs/")
async def create_dog(dog: DogSchema):
    local = next(get_db())
    length_dog = local.query(Dog).count()
    length_sight = local.query(Sighting).count()
    length_photo = local.query(Photo).count()
    sighting = Sighting(sighting_id=length_sight + 1, dog_id=length_dog + 1,
                        latitude=dog.location[0], longitude=dog.location[1])
    dog_model = Dog(dog_id=length_dog + 1, breed=dog.breed, description=dog.description,
                    status=dog.status)
    local.add(dog_model)
    local.add(sighting)
    if dog.url:
        photo = Photo(photo_id=length_photo + 1, subject_id=length_dog + 1,
                      photo_url=dog.url)
        local.add(photo)
        local.commit()
        local.refresh(photo)
    else:
        local.commit()
    local.refresh(dog_model)
    local.refresh(sighting)
    return {"dog": dog_model, "sight": sighting}


@app.post("/api/photo-upload/")
async def upload_photo(file: UploadFile = File(...)):
    print(file.filename)
    new_name = "./images/" + str(uuid.uuid4()) + file.filename
    with open(new_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": new_name}
