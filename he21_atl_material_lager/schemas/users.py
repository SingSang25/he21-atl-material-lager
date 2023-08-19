from pydantic import BaseModel
from he21_atl_material_lager.schemas.items import Item
from he21_atl_material_lager.schemas.logs import Log


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    item: list[Item] = []
    log: list[Log] = []

    class Config:
        orm_mode = True