from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from he21_atl_material_lager.models.item import Item
from he21_atl_material_lager.schemas.items import ItemCreate, ItemUpdate


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_items_by_id(db: Session, id: str):
    return db.query(Item).filter(Item.id == id).first()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(
        number=item.number,
        item=item.item,
        availability=item.availability,
        position=item.position,
        user_id=item.user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: str, item_data: ItemUpdate, db_item: Item):
    stored_item_object_schema = ItemUpdate(
        number=db_item.number,
        item=db_item.item,
        availability=db_item.availability,
        position=db_item.position,
        user_id=db_item.user_id,
    )

    updated_item_model_dump = item_data.model_dump(exclude_unset=True)

    updated_item_object_schema = stored_item_object_schema.model_copy(
        update=updated_item_model_dump
    )

    db.query(Item).filter(Item.id == item_id).update(
        jsonable_encoder(updated_item_object_schema)
    )
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: str):
    db.query(Item).filter(Item.id == item_id).delete()
    db.commit()
    return {"message": "Item deleted"}
