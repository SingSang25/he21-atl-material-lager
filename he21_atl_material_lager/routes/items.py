from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.items import Item, ItemCreate
from he21_atl_material_lager.schemas.logs import Log
from he21_atl_material_lager.services.logs import get_logs_by_item_id
from he21_atl_material_lager.services.items import (
    create_item as create_item_service,
    get_items,
    get_item,
)

router = APIRouter(prefix="/items")


# Erstellen Item
@router.post("/", response_model=Item, tags=["Item"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item_service(db=db, item=item)


# Alle Item ausgeben
@router.get("/", response_model=list[Item], tags=["Item"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_items(db, skip=skip, limit=limit)
    return users


# Ein Item Ausgeben
@router.get("/{item_id}", response_model=Item, tags=["Item"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# Log eines Items ausgeben
@router.get("/{item_id}/logs", response_model=list[Log], tags=["Item"])
def read_items_logs(item_id: int, db: Session = Depends(get_db)):
    db_user = get_logs_by_item_id(db, item_id=item_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Log by this user")
    return db_user
