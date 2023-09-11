from pydantic import BaseModel
from datetime import datetime


class LogBase(BaseModel):
    created_by: str
    user_id: str | None = None
    item_id: str | None = None
    log: str
    type: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: str
    datum: datetime

    class Config:
        from_attributes = True
