import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid

from database import Base


class Category(Base):
    __tablename__ = "categories"

    # ---------- Identifiant ----------
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    # ---------- Informations ----------
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # ---------- Relations ----------
    products = relationship("Product", back_populates="category")