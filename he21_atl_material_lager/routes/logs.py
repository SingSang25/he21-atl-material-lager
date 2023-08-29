from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.logs import Log, LogCreate
from he21_atl_material_lager.schemas.users import User
from he21_atl_material_lager.services.users import get_user_by_id
from he21_atl_material_lager.services.users_authenticate import get_current_active_user
from he21_atl_material_lager.services.items import get_items_by_id
from he21_atl_material_lager.services.logs import (
    create_log as create_log_service,
    get_logs,
    get_log,
)

router = APIRouter(prefix="/logs")


@router.post("/", response_model=Log, tags=["Log"])
def create_log(
    log: LogCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_log_user = get_user_by_id(db, log.user_id)
    db_log_item = get_items_by_id(db, log.item_id)
    if not db_log_user and not db_log_item:
        raise HTTPException(status_code=400, detail="User and Item already registered")
    if not db_log_user:
        raise HTTPException(status_code=400, detail="User not registered")

    if not db_log_item:
        raise HTTPException(status_code=400, detail="Item not registered")
    return create_log_service(db, log)


@router.get("/", response_model=list[Log], tags=["Log"])
def read_log(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/{log_id}", response_model=Log, tags=["Log"])
def read_log(
    log_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_log = get_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log
