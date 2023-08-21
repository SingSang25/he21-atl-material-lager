from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from he21_atl_material_lager.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    datum = Column(DateTime, index=True)
    log = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    user = relationship("User", back_populates="logs")
    item = relationship("Item", back_populates="logs")
