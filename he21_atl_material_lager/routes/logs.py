from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.schemas.logs import Log, LogCreate
from he21_atl_material_lager.services.logs import (
    get_logs_by_id,
    create_log as create_log_service,
    get_logs,
    get_log,
)

router = APIRouter(prefix="/logs")

@router.post("/", response_model=Log, tags=["Log"])
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = get_logs_by_id(db, id=log.id)
    if db_log:
        raise HTTPException(status_code=400, detail="Log ID already registered")
    return create_log_service(db=db, log=log)

@router.get("/", response_model=list[Log], tags=["Log"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_logs(db, skip=skip, limit=limit)
    return users


@router.get("/{logs_id}", response_model=Log, tags=["Log"])
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = get_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log