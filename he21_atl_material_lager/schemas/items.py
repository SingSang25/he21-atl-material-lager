from pydantic import BaseModel

class ItemBase(BaseModel):
    id: int
    number: int
    item: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    availability: bool

    class Config:
        orm_mode = True