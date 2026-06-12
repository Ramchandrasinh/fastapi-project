from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from .. import schemas, utils, model, oauth2

from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
SessionDep = Annotated[Session, Depends(get_db)]

@router.post("/login", response_model=schemas.Token)
def login(session: SessionDep, user_creds: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    user = session.exec(select(model.User).where(model.User.email == user_creds.username)).first()

    if not user or not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return schemas.Token(access_token=access_token, token_type="bearer")