from fastapi import FastAPI
from models import Base
from database import engine
import todo
import auth

Base.metadata.create_all(bind=engine)
app = FastAPI(title="TODOLIST API")

app.include_router(todo.router)
app.include_router(auth.router)