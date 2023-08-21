from sqlalchemy.orm import Session

from he21_atl_material_lager.models.log import Log
from he21_atl_material_lager.schemas.logs import LogCreate


def get_log(db: Session, log_id: int):
    return db.query(Log).filter(Log.id == log_id).first()


def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()


def get_logs_by_id(db: Session, id: int):
    return db.query(Log).filter(Log.id == id).first()


def get_logs_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Log).filter(Log.user_id == user_id).offset(skip).offset(limit).all()


def get_logs_by_item_id(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    return db.query(Log).filter(Log.item_id == item_id).offset(skip).offset(limit).all()


def create_log(db: Session, log: LogCreate):
    db_log = Log(datum=log.datum, log=log.log, user_id=log.user_id, item_id=log.item_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
