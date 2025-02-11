from typing import Annotated

from fastapi import APIRouter, HTTPException

from general import db_dependency
from models import TodoList
from schemas import CreateTodoSchema, UserSchema
from .auth import get_current_user

router = APIRouter(tags=["todo"], prefix="/todo")


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
async def todo_list(db: db_dependency):
	todos = db.query(TodoList).all()
	return todos


@router.get("/get/{todo_id}")
async def get_todo(todo_id: int, db: db_dependency, user: Annotated[UserSchema, get_current_user]):
	if user.role == "user":
		todo = db.query(TodoList).filter(TodoList.id == todo_id, TodoList.user_id == user.id).first()
		if todo:
			return todo
		raise HTTPException(404, detail="Todo not found")
	raise HTTPException(403, detail="Forbidden")


@router.post("/create", status_code=201)
async def create_todo(todo_schema: CreateTodoSchema, db: db_dependency,
                      user: Annotated[UserSchema, get_current_user]):
	todo = TodoList(
		title=todo_schema.title,
		description=todo_schema.description,
		priority=todo_schema.priority,
		user_id=user.id
	)
	db.add(todo)
	db.commit()
	db.refresh(todo)
	return todo


@router.put("/update/{todo_id}")
async def update_todo(todo_id: int, todo_schema: CreateTodoSchema, db: db_dependency):
	todo = db.query(TodoList).filter(TodoList.id == todo_id).first()
	if not todo:
		raise HTTPException(404, detail="Todo not found")

	for key, value in todo_schema.dict().items():
		setattr(todo, key, value)
	db.commit()
	db.refresh(todo)
	return todo


@router.delete("/delete/{todo_id}")
async def delete_todo(todo_id: int, db: db_dependency):
	todo = db.query(TodoList).filter(TodoList.id == todo_id).first()
	if not todo:
		raise HTTPException(404, detail="Todo not found")

	db.delete(todo)
	db.commit()
	return {"message": "Todo deleted"}
