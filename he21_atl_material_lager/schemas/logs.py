from pydantic import BaseModel
from datetime import date

class LogBase(BaseModel):
    id: int
    datum: date
    log: str

class LogCreate(LogBase):
    pass

class Log(LogBase):

    class Config:
        orm_mode = True