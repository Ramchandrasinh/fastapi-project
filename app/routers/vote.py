from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from typing import Annotated
from ..database import get_db
from ..model import Post, Vote
from .. import schemas, oauth2

SessionDep = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/votes", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteRequest, session: SessionDep, current_user: schemas.UserOutput = Depends(oauth2.get_current_user)):
    post = session.get(Post, vote.post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {vote.post_id} not found")

    if vote.dir == 1:
        if post.owner_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot vote on your own post")
        existing_vote = session.get(Vote, (current_user.id, vote.post_id))
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted on this post")
        new_vote = Vote(user_id=current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added"}
    else:
        existing_vote = session.get(Vote, (current_user.id, vote.post_id))
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        session.delete(existing_vote)
        session.commit()
        return {"message": "Vote removed"}
