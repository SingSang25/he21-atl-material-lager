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
)

router = APIRouter(prefix="/logs")


@router.get("/", response_model=list[Log], tags=["Log"])
def read_log(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/user/{user_id}/", response_model=list[Log], tags=["Log"])
def read_log(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_user_id(db, user_id)
    return logs


@router.get("/log_id/{log_id}/", response_model=Log, tags=["Log"])
def read_log(
    log_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_log = get_logs_by_id(db, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


@router.get("/type/{log_type}/", response_model=list[Log], tags=["Log"])
def read_log(
    log_type: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_type(db, log_type)
    return logs


@router.get("/created/{created_by}/", response_model=list[Log], tags=["Log"])
def read_log(
    created_by: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_created_by(db, created_by)
    return logs
