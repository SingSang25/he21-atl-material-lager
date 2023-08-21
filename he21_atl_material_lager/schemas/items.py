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


class Item(ItemBase):
    id: int
    log_id: list[Log] = []

    class Config:
        orm_mode = True
