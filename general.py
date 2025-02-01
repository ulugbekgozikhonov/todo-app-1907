from fastapi import Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]