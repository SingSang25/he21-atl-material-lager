from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from he21_atl_material_lager.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    items = relationship("Item", back_populates="user")
    logs = relationship("Log", back_populates="user")
