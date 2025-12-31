from app.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlmodel import Session,SQLModel

engine = create_engine(
    DATABASE_URL,
    connect_args ={"check_same_thread": False},
    echo =True
)

def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)