from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db

router = APIRouter(tags=["Filter"])

@router.get("/filters", response_model=schemas.FilterResponse)
def get_filters(db: Session = Depends(get_db)):
    formats = db.query(models.MediaFormat).all()
    genres = db.query(models.Genre).all()
    countries = db.query(models.Country).all()
    conditions = db.query(models.Condition).all()
    regions = db.query(models.Region).all()
    subtitles = db.query(models.Subtitles).all()
    packaging = db.query(models.Packaging).all()
    shipping = db.query(models.ShippingCosts).all()

    return {"Format": formats, "Genre": genres, "Country": countries, "Condition": conditions, "Region": regions, "Subtitles": subtitles, "Packaging": packaging, "Shipping": shipping}
