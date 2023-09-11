from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from he21_atl_material_lager.database import Base
from he21_atl_material_lager.dependencies import generate_uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    datum = Column(DateTime)
    log = Column(String)
    type = Column(String)  # item, user, system
    created_by = Column(String, ForeignKey("users.id"))
    user_id = Column(String, ForeignKey("users.id"))
    item_id = Column(String, ForeignKey("items.id"), nullable=True)

    user = relationship("User", back_populates="logs")
    item = relationship("Item", back_populates="logs")
