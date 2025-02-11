from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:root_123@localhost:5432/todos"
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(url=DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
