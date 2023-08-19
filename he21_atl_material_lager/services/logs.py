from sqlalchemy.orm import Session

from he21_atl_material_lager.models.log import Log
from he21_atl_material_lager.schemas.logs import LogCreate

def get_log(db: Session, log_id: int):
    return db.query(Log).filter(Log.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()

def get_logs_by_id(db: Session, id: int):
    return db.query(Log).filter(Log.id == id).first()   

def create_log(db: Session, log: LogCreate):
    db_log = Log(id=log.id, datum=log.datum, log=log.log)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log