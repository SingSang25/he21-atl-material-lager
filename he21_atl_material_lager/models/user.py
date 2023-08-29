from uuid import uuid4
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from he21_atl_material_lager.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)

    items = relationship("Item", back_populates="user")
    logs = relationship("Log", back_populates="user")
