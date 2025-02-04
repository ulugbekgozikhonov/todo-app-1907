from fastapi import APIRouter,Request,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from general import db_dependency
from models import TodoList
from schemas import CreateTodoSchema
from .auth import decode_access_token
from typing import Annotated
from .auth import get_current_user

router = APIRouter(tags=["todo"],prefix="/todo")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
token_dependency = Annotated[str,Depends(oauth2_scheme)]

# @router.get("/list")
# async def todo_list(db: db_dependency,request: Request):
#     authorization = request.headers.get("Authorization")
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Authorization header is missing")
    
#     token = authorization[7:]
#     payload = decode_access_token(token)
#     user = get_current_user(payload)
#     todos = db.query(TodoList).all()
#     return todos

@router.get("/list")
async def todo_list(db: db_dependency,token: token_dependency):
    payload = decode_access_token(token)
    user = get_current_user(payload,db)
    if user.role == "user":
        todos = db.query(TodoList).all()
        return todos
    raise HTTPException(403,detail="Forbidden")

@router.post("/create")
async def create_todo(todo_schema: CreateTodoSchema,db:db_dependency):
    pass    