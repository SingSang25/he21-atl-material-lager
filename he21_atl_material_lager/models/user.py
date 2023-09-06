from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.dependencies import generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)

    items = relationship("Item", back_populates="user")
    logs = relationship("Log", back_populates="user")
