from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.items import Item, ItemCreate, ItemUpdate
from he21_atl_material_lager.schemas.logs import Log, LogCreate
from he21_atl_material_lager.schemas.users import User
from he21_atl_material_lager.services.logs import (
    get_logs_by_item_id,
    create_log as create_log_service,
)
from he21_atl_material_lager.services.users import is_user_admin
from he21_atl_material_lager.services.users_authenticate import get_current_active_user
from he21_atl_material_lager.services.items import (
    create_item as create_item_service,
    update_item as update_item_service,
    delete_item as delete_item_service,
    get_items,
    get_items_by_id,
)

router = APIRouter(prefix="/items")


@router.patch("/{item_id}/", response_model=Item, tags=["Item"])
def update_item(
    item_data: ItemUpdate,
    item_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_item = get_items_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item = update_item_service(db, item_id, item_data, db_item)
    create_log_service(
        db,
        LogCreate(
            created_by=current_user.id, item_id=item.id, log="Item updated", type="item"
        ),
    )
    return item


@router.post("/", response_model=Item, tags=["Item"])
def create_item(
    item: ItemCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if is_user_admin(db, current_user.id) is False:
        raise HTTPException(status_code=400, detail="Activ User is not an Admin")
    item = create_item_service(db=db, item=item)
    create_log_service(
        db,
        LogCreate(
            created_by=current_user.id,
            item_id=item.id,
            log="Item created",
            type="item",
        ),
    )
    return item


@router.get("/", response_model=list[Item], tags=["Item"])
def read_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = get_items(db, skip=skip, limit=limit)
    return users


@router.get("/{item_id}/", response_model=Item, tags=["Item"])
def read_item(
    item_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_item = get_items_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/{item_id}/logs/", response_model=list[Log], tags=["Item"])
def read_items_logs(
    item_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_logs_by_item_id(db, item_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Log by this item found")
    return db_user


@router.delete("/{item_id}/", response_model=dict, tags=["Item"])
def delete_item(
    item_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if is_user_admin(db, current_user.id) is False:
        raise HTTPException(status_code=400, detail="Activ User is not an Admin")
    db_item = get_items_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item = delete_item_service(db, item_id)
    create_log_service(
        db,
        LogCreate(
            created_by=current_user.id, item_id=item_id, log="Item deleted", type="item"
        ),
    )
    return item
