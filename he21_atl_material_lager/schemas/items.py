from pydantic import BaseModel
from he21_atl_material_lager.schemas.logs import Log


class ItemBase(BaseModel):
    number: int
    item: str
    availability: bool
    position: str
    user_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    number: int | None = None
    item: str | None = None
    availability: bool | None = None
    position: str | None = None
    user_id: int | None = None


class Item(ItemBase):
    id: int
    log_id: list[Log] = []

    class Config:
        orm_mode = True
