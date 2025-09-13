from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,TIMESTAMP
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship

# Creates a class called User that has attributes to create a table called 'users' in the database.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    username = Column(String, unique = True, index = True)
    email = Column(String, unique = True, index = True)

    # I don't really know how to work with these two
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)

    album = relationship("Album", back_populates="user", cascade="all, delete-orphan")
    image = relationship("Image", back_populates="user", cascade="all, delete-orphan")


class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    createtime = Column(TIMESTAMP(timezone=True), nullable=False, default = datetime.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index = True)
    privacy = Column(String, index = True, default = "Private")
    user = relationship("User", back_populates="album")
    image = relationship("Image", back_populates="album", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    posttime = Column(TIMESTAMP(timezone=True), nullable=False, default = datetime.now())
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), index = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index = True)
    privacy = Column(String, index = True, default = "Private")
    mimetype = Column(String, index = True)
    size_in_percentage = Column(Integer, index = True, default = 100)
    original_width = Column(Integer, index = True)
    original_height = Column(Integer, index = True)
    width = Column(Integer, index = True)
    height = Column(Integer, index = True)
    user = relationship("User", back_populates="image")
    album = relationship("Album", back_populates="image")