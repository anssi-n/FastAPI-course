from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . config import settings

DB_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DB_URL, echo=True)

session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
