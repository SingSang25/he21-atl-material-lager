from fastapi import APIRouter
from he21_atl_material_lager.schemas.items import Item, ItemCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.items import (
    get_items_by_id,
    create_item as create_item_service,
    get_items,
    get_item,
)
from he21_atl_material_lager.services.items import create_item

router = APIRouter(prefix="/items")

@router.post("/", response_model=Item)
def creat_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = get_items_by_id(db, id=item.id)
    if db_item:
        raise HTTPException(status_code=400, detail="Item ID already registered")
    return create_item_service(db=db, item=item)

@router.get("/", response_model=list[Item])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_items(db, skip=skip, limit=limit)
    return users


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item