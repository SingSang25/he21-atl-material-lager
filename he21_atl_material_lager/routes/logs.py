from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.logs import Log
from he21_atl_material_lager.schemas.users import User
from he21_atl_material_lager.services.users_authenticate import get_current_active_user
from he21_atl_material_lager.services.logs import get_logs, get_log, get_logs_by_type

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


@router.get("/{log_type}", response_model=list[Log], tags=["Log"])
def read_log(
    log_type: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logs = get_logs_by_type(db, type=log_type)
    return logs
