from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter( tags=["Voting"])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote( vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.item_id == vote.item_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {current_user.id} has already voted on item {vote.item_id}.")
        new_vote = models.Vote( item_id=vote.item_id, user_id=current_user.id )

        try:
            db.add(new_vote)
            db.commit()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item {vote.item_id} does not exist.")
        return { "message" : "Succesfully voted!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return { "message" : "Succesfully deleted vote!"}
