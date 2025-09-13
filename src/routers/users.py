from ..models import User
from ..schemas import UserCreate, UserResponse, UserInDB, UserUpdate
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List

# You can define normal un-router functions in utils.py. To use: use it as utils.function()
from .. import utils

user_router = APIRouter()

@user_router.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Emal address already registered")
    
    # I've commented out the password stuff for now, I've yet to understand it
    
    # hashed_pass = get_password_hash(user.password)

    # I've said hashed_password = password (whatever user has given) for now. Need to change it to hashed password after writing hashing code.
    db_user = User(name = user.name, username = user.username, email = user.email, hashed_password = user.password) # hashed_password = hashed_pass
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.get("/users/", response_model = List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@user_router.get("/users/{user_id}", response_model = UserResponse)
def read_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name if user.name != "" else db_user.name
    db_user.username = user.username if user.username != "" else db_user.username
    db_user.email = user.email if user.email != "" else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id:int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    utils.delete_album_by_user(user_id, db)
    db.delete(db_user)
    db.commit()
    return db_user