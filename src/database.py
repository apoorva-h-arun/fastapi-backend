from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Creating a local SQLite database called 'test'
# DATABASE_URL = "postgresql://postgres:testdatabase@localhost:5432/testdb"
DATABASE_URL = "postgresql://neondb_owner:npg_jyYMv0OAp3Wb@ep-summer-truth-adbe6t13-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

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