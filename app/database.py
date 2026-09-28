"""Database configuration for WMS Operacional."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./wms_demo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()