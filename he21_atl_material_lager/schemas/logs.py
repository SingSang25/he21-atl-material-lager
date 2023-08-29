from pydantic import BaseModel
from datetime import datetime


class LogBase(BaseModel):
    user_id: int
    item_id: int
    log: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int
    datum: datetime

    class Config:
        orm_mode = True
