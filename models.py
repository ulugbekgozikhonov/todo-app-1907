from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime

class TodoList(Base):
    __tablename__ = "todo_list"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=100), nullable=False, index=True)
    priority = Column(Integer, nullable=False, index=True)
    description = Column(String(length=255))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime,nullable=False,default=datetime.now)
    updated_at = Column(DateTime,nullable=False, default=datetime.now, onupdate=datetime.now)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    first_name = Column(String(length=50), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(length=55), nullable=False, default="user")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)