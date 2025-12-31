from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables

from app.models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="MentorQ", lifespan=lifespan)

@app.get("/")
def root():
    return {"message":"MentorQ API"}

