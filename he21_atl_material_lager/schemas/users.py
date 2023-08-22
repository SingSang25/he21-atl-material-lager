from pydantic import BaseModel
from he21_atl_material_lager.schemas.items import Item
from he21_atl_material_lager.schemas.logs import Log

class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None = None
    username: str | None = None
    password: str | None = None


class User(UserBase):
    id: int
    item_id: list[Item] = []
    log_id: list[Log] = []

    class Config:
        orm_mode = True
