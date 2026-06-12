from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Annotated, Optional
from ..database import get_db
from ..model import Post, Vote
from .. import schemas, oauth2

SessionDep = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(session: SessionDep, limit: int = 10, skip: int = 0, search: str = "") -> list[schemas.PostResponse]:
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))  # type: ignore
        .join(Vote, Vote.post_id == Post.id, isouter=True)  # type: ignore
        .group_by(Post.id)  # type: ignore
        .where(Post.title.contains(search))  # type: ignore
        .offset(skip)
        .limit(limit)
    )

    results = session.exec(statement).all()

    return [
        schemas.PostResponse.model_validate({**post.model_dump(), "votes": votes, "owner": post.owner})
        for post, votes in results
    ]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, session: SessionDep, current_user: schemas.UserOutput = Depends(oauth2.get_current_user)) -> schemas.PostResponse:
    db_post = Post.model_validate(post)
    db_post.owner_id = current_user.id
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return schemas.PostResponse.model_validate(db_post)

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, session: SessionDep) -> schemas.PostResponse:
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))  # type: ignore
        .join(Vote, Vote.post_id == Post.id, isouter=True)  # type: ignore
        .group_by(Post.id) # type: ignore
        .where(Post.id == id) # type: ignore
    ) 
    post, votes = session.exec(statement).first() #type: ignore
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")
    # return schemas.PostResponse.model_validate({**post.model_dump(), "votes": votes})
    return schemas.PostResponse.model_validate({**post.model_dump(), "votes": votes, "owner": post.owner})

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_post(id: int, session: SessionDep, current_user: schemas.UserOutput = Depends(oauth2.get_current_user)) -> Response:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated: schemas.PostUpdate, session: SessionDep, current_user: schemas.UserOutput = Depends(oauth2.get_current_user)) -> schemas.PostResponse:
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post.sqlmodel_update(updated.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(post)
    return schemas.PostResponse.model_validate(post)