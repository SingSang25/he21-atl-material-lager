from pydantic import BaseModel
from datetime import datetime


class LogBase(BaseModel):
    datum: datetime
    user_id: int
    item_id: int
    log: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int

    class Config:
        orm_mode = True
