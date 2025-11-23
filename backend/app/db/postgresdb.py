from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends
from app.core.config import config

from contextlib import contextmanager

engine = create_engine(
    config.DATABASE_URL,
    echo=False,
    future=True,
)
session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

@contextmanager
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

dbSession = Annotated[Session, Depends(get_db)]


