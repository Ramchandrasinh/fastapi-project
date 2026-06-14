from fastapi import FastAPI, Depends
from sqlmodel import Session
from typing import Annotated
from .database import create_db_and_tables, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SessionDep = Annotated[Session, Depends(get_db)]

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root() -> dict:
    return {"msg": "Hello World"}

