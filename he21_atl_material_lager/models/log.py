from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from he21_atl_material_lager.database import Base
from he21_atl_material_lager.dependencies import generate_uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    datum = Column(DateTime, index=True)
    log = Column(String, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    item_id = Column(String, ForeignKey("items.id"))

    user = relationship("User", back_populates="logs")
    item = relationship("Item", back_populates="logs")
