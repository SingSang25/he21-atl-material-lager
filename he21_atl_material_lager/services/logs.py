from sqlalchemy.orm import Session
from datetime import datetime

from he21_atl_material_lager.models.log import Log
from he21_atl_material_lager.schemas.logs import LogCreate


def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()


def get_logs_by_id(db: Session, id: str):
    return db.query(Log).filter(Log.id == id).first()


def get_logs_by_user_id(db: Session, user_id: str):
    return db.query(Log).filter(Log.user_id == user_id).all()


def get_logs_by_item_id(db: Session, item_id: str):
    return db.query(Log).filter(Log.item_id == item_id)


def get_logs_by_type(db: Session, type: str):
    return db.query(Log).filter(Log.type == type).all()


def get_logs_by_created_by(db: Session, created_by: str):
    return db.query(Log).filter(Log.created_by == created_by).all()


def create_log(db: Session, log: LogCreate):
    db_log = Log(
        **log.model_dump(),
        datum=datetime.today(),
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
