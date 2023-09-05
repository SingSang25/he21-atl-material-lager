from pydantic import BaseModel
from he21_atl_material_lager.schemas.items import Item
from he21_atl_material_lager.schemas.logs import Log


class UserBase(BaseModel):
    email: str
    username: str
    admin: bool
    disabled: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    admin: bool | None = None
    disabled: bool | None = None


class User(UserBase):
    id: str
    item: list[Item] = []
    log: list[Log] = []

    class Config:
        from_attributes = True
