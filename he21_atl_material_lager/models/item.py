from sqlalchemy import Column, Integer, String

from he21_atl_material_lager.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    number = Column(Integer, index=True)
    position = Column(String, index=True)