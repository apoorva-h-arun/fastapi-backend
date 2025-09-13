from .models import User, Album, Image
from fastapi import Depends, HTTPException, UploadFile
import mimetypes
from sqlalchemy.orm import Session
from .database import get_db
import os

# This is the space to put all random functions

'''def get_password_hash(password):
    return pwd_context.hash(password)'''

# (Can change the contents of this list if needed)
album_privacy_list = ["private", "public", "unlisted"]
image_privacy_list = ["private", "public", "unlisted"]

def check_image_type(img: UploadFile):
    if img.content_type.split('/')[0] == "image":
        return True
    else:
        return False
    
def compare_type(oldname: str, newname: str):
    old_type = mimetypes.guess_type(oldname)
    if mimetypes.guess_type(newname)[0] == None:
        return (newname + mimetypes.guess_extension(old_type[0]))
    if old_type == mimetypes.guess_type(newname):
        return newname
    else:
        return None

def delete_images_by_album(album_id: int, db: Session = Depends(get_db)):
    image_list = db.query(Image).filter(Image.album_id == album_id).all()
    for image in image_list:
        os.remove(f"./uploads/{image.name}")

def delete_album_by_user(user_id: int, db: Session = Depends(get_db)):
    album_list = db.query(Album).filter(Album.user_id == user_id).all()
    for album in album_list:
        delete_images_by_album(album.id, db)