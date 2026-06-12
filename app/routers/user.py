from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlmodel import Session, select
from typing import Annotated
from ..database import get_db
from ..model import User
from .. import utils, schemas

SessionDep = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.UserOutput])
def get_users(session: SessionDep) -> list[schemas.UserOutput]:
    users = session.exec(select(User)).all()
    return [schemas.UserOutput.model_validate(user) for user in users]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserBase, session: SessionDep) -> schemas.UserOutput:
    user.password = utils.hash_password(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return schemas.UserOutput.model_validate(db_user)

@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, session: SessionDep) -> schemas.UserOutput:
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    return schemas.UserOutput.model_validate(user)