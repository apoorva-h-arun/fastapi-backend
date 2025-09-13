from fastapi import FastAPI
from src.database import Base, engine
from src import models
from src.routers.users import user_router
from src.routers.albums import album_router
from src.routers.images import image_router

app = FastAPI()

# Actually creates the tables (specified in models.py) in the database
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(album_router)
app.include_router(image_router)

@app.post("/")
def display():
    return{"message": "Hello World!"}