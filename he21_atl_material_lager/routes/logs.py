from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.logs import Log, LogCreate
from he21_atl_material_lager.services.users import get_users_by_id
from he21_atl_material_lager.services.items import get_items_by_id
from he21_atl_material_lager.services.logs import (
    create_log as create_log_service,
    get_logs,
    get_log,
)

router = APIRouter(prefix="/logs")


@router.post("/", response_model=Log, tags=["Log"])
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = get_users_by_id(db, id=log.user_id)
    if not db_log:
        raise HTTPException(status_code=400, detail="User not registered")
    db_log = get_items_by_id(db, id=log.item_id)
    if not db_log:
        raise HTTPException(status_code=400, detail="Item not registered")
    return create_log_service(db=db, log=log)


@router.get("/", response_model=list[Log], tags=["Log"])
def read_log(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/{log_id}", response_model=Log, tags=["Log"])
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = get_log(db, logs_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log
