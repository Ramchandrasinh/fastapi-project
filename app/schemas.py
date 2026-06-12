from sqlmodel import SQLModel, Field
from pydantic import EmailStr, ConfigDict
from datetime import datetime
from typing import Annotated

class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class UserOutput(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutput
    votes: int = 0

    model_config = ConfigDict(from_attributes=True) # type: ignore

class UserBase(SQLModel):
    id: int | None = None
    email: EmailStr
    password: str

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: int | None = None

class VoteRequest(SQLModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]
    