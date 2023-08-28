from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import functions, text
from .. import models, schemas, oauth2
from .. database import get_db
from typing import List

router = APIRouter(prefix="/items", tags=["Items"])

# Create


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO item (item_description, item_format, item_genre, item_country, item_region, item_subtitles, item_packaging,
    #                     item_slipcover, item_condition, item_condition_comment, item_images, item_price, item_shipping, item_huuto_id, item_huuto_text,
    #                     item_huuto_endtime, item_modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""", (
    #                     new_item.item_description, new_item.item_format, new_item.item_genre, new_item.item_country, new_item.item_region, new_item.item_subtitles,
    #                     new_item.item_packaging, new_item.item_slipcover, new_item.item_condition, new_item.item_condition_comment, new_item.item_images,
    #                     new_item.item_price, new_item.item_shipping, new_item.item_huuto_id, new_item.item_huuto_text, new_item.item_huuto_endtime, new_item.item_modified))
    # added_item = new_item.model_dump()
    # added_item['item_id'] = cursor.lastrowid
    # db_conn.commit()
    print(f"Current user={current_user}")
    new_item = models.Item(owner_id=current_user.id, **item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Read, all

@router.get("/count", response_model=schemas.ItemCount)
def get_items(db: Session = Depends(get_db)):
    item_count = db.query(models.Item).count()
    return { "item_count" : item_count } 

@router.get("/", response_model=List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db), limit: int | None = None, skip: int | None = None, search: str = ""):
    # cursor.execute("SELECT * FROM item WHERE item_price > 70")
    # items = cursor.fetchall()
    items = db.query(models.Item).filter(
        models.Item.item_description.contains(search)).limit(limit).offset(skip).all()

    return items

# Read, one


@router.get("/{id}")
# @router.get("/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM item WHERE item_id = %s", (id,))
    # item = cursor.fetchone()
    # db_conn.commit()
    # if item is not None:
    #     return { "data": item}
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Item with id {id} does not exist.")
    
    #select item.*, count(votes.item_id) as likes from item left join votes on item.item_id = votes.item_id group by item.item_id;
    item = db.query(models.Item).filter(models.Item.item_id == id).first()
    #item = db.query(models.Item, functions.count(models.Vote.item_id).label("likes")).join(models.Vote, isouter=True).filter(models.Item.item_id == id).first()
    #item = db.query(models.Item, models.MediaFormat).join(models.MediaFormat, isouter=True).filter(models.Item.item_id == id).first()
    #item = db.query(models.Item.item_description, models.MediaFormat.format_name.label("item_item_formaatti")).apply_labels().join(models.MediaFormat, isouter=True).filter(models.Item.item_id == id).first()

    if item is not None:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} does not exist.")

# Update


@router.put("/{id}", response_model=schemas.ItemResponse)
def update_item(id: int, update_data: schemas.ItemCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE item SET item_description=%s, item_format=%s, item_genre=%s, item_country=%s, item_region=%s, item_subtitles=%s, item_packaging=%s,
    #                     item_slipcover=%s, item_condition=%s, item_condition_comment=%s, item_images=%s, item_price=%s, item_shipping=%s, item_huuto_id=%s,
    #                     item_huuto_text=%s, item_huuto_endtime=%s, item_modified=%s WHERE item_id=%s""", (
    #                     update_data.item_description, update_data.item_format, update_data.item_genre, update_data.item_country, update_data.item_region,
    #                     update_data.item_subtitles, update_data.item_packaging, update_data.item_slipcover, update_data.item_condition, update_data.item_condition_comment,
    #                     update_data.item_images, update_data.item_price, update_data.item_shipping, update_data.item_huuto_id, update_data.item_huuto_text,
    #                     update_data.item_huuto_endtime, update_data.item_modified, id))
    # updated_rows = cursor.rowcount
    # db_conn.commit()
    item_query = db.query(models.Item).filter(models.Item.item_id == id)
    item = item_query.first()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} does not exist.")

    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform current action.")

    updated_data = update_data.model_dump()
    item_query.update(updated_data, synchronize_session=False)
    db.commit()
    return item_query.first()


# Delete
@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM item WHERE item_id = %s", (id,))
    # deleted_rows = cursor.rowcount
    # db_conn.commit()
    # if deleted_rows == 1:
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Item with id {id} does not exist.")
    item_query = db.query(models.Item).filter(models.Item.item_id == id)
    item = item_query.first()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} does not exist.")

    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform current action.")

    item_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
