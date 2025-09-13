from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#-------USER---------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    username: str

class UserInDB(UserResponse):
    is_active: bool
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None

#-------ALBUM--------------------------------------------------------------------

class AlbumCreate(BaseModel):
    name: str
    privacy: str

class AlbumResponse(BaseModel):
    id: int
    name: str
    createtime: datetime
    user_id: int
    privacy: str
    
class AlbumUpdate(BaseModel):
    name: Optional[str] = None
    privacy: Optional[str] = None

#-------IMAGE--------------------------------------------------------------------

class ImageResponse(BaseModel):
    id: int
    name: str
    posttime: datetime
    album_id: int
    user_id: int
    privacy: str
    mimetype: str
    size_in_percentage: int
    original_width: int
    original_height: int
    width: int
    height: int
    
class ImageUpdate(BaseModel):
    name: Optional[str] = None
    privacy: Optional[str] = None
    size_in_percentage: Optional[int] = None