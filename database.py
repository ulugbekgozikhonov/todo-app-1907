from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://todo_user:3Mu9aiAs4uMv5sYfHMbAhSds3wlwqd3e@dpg-culkrft2ng1s73atgm1g-a.oregon-postgres.render.com/todos_3epo"
# DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(url=DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
