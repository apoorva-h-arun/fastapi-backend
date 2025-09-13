from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Creating a local SQLite database called 'test'
DATABASE_URL = "postgresql://postgres:testdatabase@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Function to open a session to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()