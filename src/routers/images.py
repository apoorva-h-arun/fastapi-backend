from ..models import User, Album, Image
from ..schemas import ImageResponse, ImageUpdate
from ..database import get_db
#from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from typing import List
from PIL import Image as Img
from typing import Optional
import os

# You can define normal un-router functions in utils and use it here
from .. import utils

image_router = APIRouter()

@image_router.post("/{user_name}/{album_id}/upload/", response_model=ImageResponse)
def upload_image(user_name: str, album_id: int, privacy: Optional[str] = None, size: Optional[int] = None, image: UploadFile = File(...), db: Session = Depends(get_db)):

    if utils.check_image_type(image) is False:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    user_check = db.query(User).filter(User.name == user_name).first()
    if user_check is None:
        raise HTTPException(status_code=400, detail="Invalid username.")

    album_check = db.query(Album).filter(Album.id == album_id).first()
    if album_check is None:
        raise HTTPException(status_code=400, detail="Invalid album ID.")

    db_img = db.query(Image).filter(Image.name == image.filename).first()
    if db_img is not None:
        raise HTTPException(status_code=400, detail="Cannot have two images of the same name.")
    
    if privacy is None:
        privacy = album_check.privacy
    elif privacy not in utils.image_privacy_list:
        raise HTTPException(status_code=400, detail="Invalid privacy setting")
    
    with open(f'./uploads/{image.filename}', "wb") as f:
        f.write(image.file.read())
    img = Img.open(f'./uploads/{image.filename}')
    if size is None:
        size = 100
    orig_w, orig_h = img.size
    w = int(orig_w * size / 100)
    h = int(orig_h * size / 100)
    if size is not None:
        img.resize((w, h))

    db_image = Image(
        name = image.filename,
        album_id = album_id,
        user_id = user_check.id,
        privacy = privacy,
        mimetype = image.content_type,
        size_in_percentage = size,
        original_width = orig_w,
        original_height = orig_h,
        width = w,
        height = h
    )

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

    # So the privacy thing is still sketchy. Need to somehow verify if the person has access to edit.

@image_router.get("/{album_id}/images/", response_model = List[ImageResponse])
def read_images_in_album(album_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    images = db.query(Image).filter(Image.album_id == album_id).offset(skip).limit(limit).all()
    return images

@image_router.get("/{user_id}/images/user", response_model = List[ImageResponse])
def read_all_images_by_user(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    images = db.query(Image).filter(Image.user_id == user_id).offset(skip).limit(limit).all()
    return images

@image_router.get("/images/{album_id}", response_model = ImageResponse)
def read_image_by_id(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@image_router.get("/images/", response_model = List[ImageResponse])
def read_image_by_name(image_name: str, db: Session = Depends(get_db)):
    images = db.query(Image).filter(Image.name == image_name).all()
    if images is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return images

# Can't change the image itself, but can rename it and change privacy and size (as a percentage relative to original).
@image_router.put("/images/{image_id}", response_model=ImageResponse)
def update_image(image_id: int, image: ImageUpdate, db: Session = Depends(get_db)):

    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    name_with_type = utils.compare_type(db_image.name, image.name)
    if not name_with_type:
        raise HTTPException(status_code=400, detail="Invalid type suffix.")
    else:
        image.name = name_with_type
    
    if image.size_in_percentage is not None:
        db_image.size_in_percentage = image.size_in_percentage
        w = int(db_image.original_width * image.size_in_percentage / 100)
        h = int(db_image.original_height * image.size_in_percentage / 100)
        img = Img.open(f'./uploads/{db_image.name}')
        resized_img = img.resize((w, h))
        resized_img.save(f'./uploads/{db_image.name}')
        db_image.width = w
        db_image.height = h

    if image.name is not None:
        os.rename(f'./uploads/{db_image.name}', f'./uploads/{image.name}')
        db_image.name = image.name

    if image.privacy is not None and image.privacy in utils.album_privacy_list:
        db_image.privacy = image.privacy

    db.commit()
    db.refresh(db_image)
    return db_image

@image_router.delete("/images/{image_id}", response_model=ImageResponse)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(f"./uploads/{db_image.name}")
    db.delete(db_image)
    db.commit()
    return db_image