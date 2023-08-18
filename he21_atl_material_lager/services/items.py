from sqlalchemy.orm import Session

from he21_atl_material_lager.models.item import Item
from he21_atl_material_lager.schemas.items import ItemCreate

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_items_by_id(db: Session, id: int):
    return db.query(Item).filter(Item.id == id).first()   

def create_item(db: Session, item: ItemCreate):
    db_item = Item(number=item.number, item=item.item, id=item.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item