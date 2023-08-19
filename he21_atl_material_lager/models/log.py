from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from he21_atl_material_lager.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    datum = Column(DateTime, index=True)
    log = Column(String, index=True)

    items = relationship("Item", back_populates="log")
    user = relationship("User", back_populates="log")