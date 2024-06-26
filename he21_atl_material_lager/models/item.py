from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.dependencies import generate_uuid


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    item = Column(String)
    number = Column(Integer)
    position = Column(String)
    availability = Column(Boolean)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="items")
    logs = relationship("Log", back_populates="item")
