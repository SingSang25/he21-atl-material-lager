from pydantic import BaseModel
from datetime import date


class LogBase(BaseModel):
    datum: date
    user_id: int
    item_id: int
    log: str


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int

    class Config:
        orm_mode = True
