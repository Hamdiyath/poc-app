import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid

from database import Base


class Product(Base):
    __tablename__ = "products"

    # ---------- Identifiant ----------
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    # ---------- Informations ----------
    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, index=True)
    stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    # ---------- Clé étrangère ----------
    category_id = Column(Uuid, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)

    # ---------- Horodatage ----------
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # ---------- Relations ----------
    category = relationship("Category", back_populates="products")