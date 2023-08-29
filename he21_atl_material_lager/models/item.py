from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from he21_atl_material_lager.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    item = Column(String, index=True)
    number = Column(Integer, index=True)
    position = Column(String, index=True)
    availability = Column(Boolean, index=True)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="items")
    logs = relationship("Log", back_populates="item")
