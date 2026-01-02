from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, ticket

import app.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="MentorQ", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ticket.router, prefix="/ticket", tags=["ticket"])

@app.get("/")
def root():
    return {"message":"MentorQ API"}

