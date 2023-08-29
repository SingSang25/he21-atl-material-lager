from pydantic import BaseModel
from datetime import datetime


class LogBase(BaseModel):
    user_id: str
    item_id: str
    log: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: str
    datum: datetime

    class Config:
        orm_mode = True
