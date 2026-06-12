from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Boolean, DateTime, text
from datetime import datetime
from typing import Optional, List

class Post(SQLModel, table=True):

    __tablename__ = "posts"  # type: ignore
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str
    content: str
    published: bool | None = Field(
        default=None,
        sa_column=Column(Boolean, server_default=text("True"), nullable=False)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    )
    owner_id: int | None = Field(default=None, nullable=False, foreign_key="users.id", ondelete="CASCADE")

    owner: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):

    __tablename__ = "users"  # type: ignore
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    )

    posts: List["Post"] = Relationship(back_populates="owner")

class Vote(SQLModel, table=True):

    __tablename__ = "votes"  # type: ignore
    user_id: int | None = Field(default=None, nullable=False, foreign_key="users.id", ondelete="CASCADE", primary_key=True)
    post_id: int | None = Field(default=None, nullable=False, foreign_key="posts.id", ondelete="CASCADE", primary_key=True)
