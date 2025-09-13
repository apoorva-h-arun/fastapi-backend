from ..models import User, Album, Image
from ..schemas import AlbumCreate, AlbumResponse, AlbumUpdate
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List

# You can define normal un-router functions in utils and use it here
from .. import utils

album_router = APIRouter()

@album_router.post("/{user_name}/albums/", response_model=AlbumResponse)
def create_album(user_name: str, album: AlbumCreate, db: Session = Depends(get_db)):

    # I guess we can have different albums with the same name? What if 3 different people want to create an album called 'flowers'
    '''db_album = db.query(Album).filter(Album.name == album.name).first()
    if db_album:
        raise HTTPException(status_code=400, detail="Username already registered")'''
    
    user = db.query(User).filter(User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if album.privacy not in utils.album_privacy_list:
        raise HTTPException(status_code=404, detail="Invalid privacy setting")
    db_album = Album(name = album.name, privacy = album.privacy, user_id = user.id)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@album_router.get("/{user_id}/albums/", response_model = List[AlbumResponse])
def read_albums_by_user(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    albums = db.query(Album).filter(Album.user_id == user_id).offset(skip).limit(limit).all()
    return albums

@album_router.get("/albums/", response_model = List[AlbumResponse])
def read_all_albums(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    albums = db.query(Album).offset(skip).limit(limit).all()
    return albums

@album_router.get("/{user_name}/albums/{album_id}", response_model = AlbumResponse)
def read_album_by_id(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@album_router.get("/{user_name}/albums/", response_model = AlbumResponse)
def read_album(album_name: str, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.name == album_name).all()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@album_router.put("/{user_name}/albums/{album_id}", response_model=AlbumResponse)
def update_album(album_id: int, album: AlbumUpdate, db: Session = Depends(get_db)):
    # Need to call get_current_user here. That function is yet to be written

    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Updates information only if given
    if album.name is not None:
        db_album.name = album.name
    if album.privacy is not None and album.privacy in utils.album_privacy_list:
        db_album.privacy = album.privacy

    db.commit()
    db.refresh(db_album)
    return db_album

@album_router.delete("/{user_name}/albums/{album_id}", response_model=AlbumResponse)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    utils.delete_images_by_album(album_id, db)
    db.delete(db_album)
    db.commit()
    return db_album