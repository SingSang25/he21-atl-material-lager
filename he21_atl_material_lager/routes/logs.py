from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.logs import Log
from he21_atl_material_lager.schemas.users import User
from he21_atl_material_lager.services.users_authenticate import get_current_active_user
from he21_atl_material_lager.services.logs import (
    get_logs,
    get_logs_by_type,
    get_logs_by_created_by,
    get_logs_by_user_id,
    get_logs_by_id,
    get_logs_by_item_id,
)

router = APIRouter()


@router.get("/logs/", response_model=list[Log], tags=["Log"])
def read_log(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/logs/{log_id}/", response_model=Log, tags=["Log"])
def read_log(
    log_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_log = get_logs_by_id(db, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


@router.get("/logs/type/{log_type}/", response_model=list[Log], tags=["Log"])
def read_log(
    log_type: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_type(db, log_type)
    if logs is None:
        raise HTTPException(status_code=404, detail="No Log by type found")
    return logs


@router.get("/logs/created/{created_by}/", response_model=list[Log], tags=["Log"])
def read_log(
    created_by: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_created_by(db, created_by)
    if logs is None:
        raise HTTPException(status_code=404, detail="No Log by created found")
    return logs


@router.get("/items/{item_id}/logs/", response_model=list[Log], tags=["Item"])
def read_items_logs(
    item_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_logs_by_item_id(db, item_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Log by this item found")
    return db_user


@router.get("/users/{user_id}/logs/", response_model=list[Log], tags=["User"])
def read_log(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_user_id(db, user_id)
    if logs is None:
        raise HTTPException(status_code=404, detail="No Log by this user found")
    return logs
