from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from general import get_db
from main import app

client = TestClient(app)

from database import Base

DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
	DATABASE_URL,
	connect_args={"check_same_thread": False},
	poolclass=StaticPool,
)
Base.metadata.create_all(engine)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def override_get_db():
	db = TestingSessionLocal()
	try:
		yield db
	finally:
		db.close()


# def override_get_current_user():
# 	db = TestingSessionLocal()
# 	try:
# 		user = db.query(User).filter(User.id == 1).first()
# 	finally:
# 		db.close()
# 	return user


app.dependency_overrides = {get_db: override_get_db}


# app.dependency_overrides = {get_current_user: override_get_current_user}


def test_todo_list():
	token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkwMTk2ODl9.V5Ook1jD6BnZUnA5HTY_4qSvHhO2S02ti6ZqR21jZv0'
	response = client.get("todo/list", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert response.json() == []


def test_todo_by_id():
	token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkwMTk2ODl9.V5Ook1jD6BnZUnA5HTY_4qSvHhO2S02ti6ZqR21jZv0'
	response = client.get("todo/get/1", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 404
	assert response.json() == {"detail": "Todo not found"}


def test_create_todo():
	token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJrZXRtb24iLCJleHAiOjE3MzkwMTk2ODl9.V5Ook1jD6BnZUnA5HTY_4qSvHhO2S02ti6ZqR21jZv0'
	todo = {
		"title": "Lear Git",
		"description": "asdfghjkl",
		"priority": 5,
		"user_id": 1
	}

	response = client.post("todo/create", json=todo, headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 201
	assert len(response.json()) > 0
