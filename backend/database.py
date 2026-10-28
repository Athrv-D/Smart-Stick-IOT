import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./smart_stick.db" if USE_SQLITE else "postgresql://smartstick:smartstick@localhost:5432/smartstick_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
