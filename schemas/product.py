from typing import Optional
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Données communes d'un produit (création et mise à jour)."""
    title: str = Field(..., max_length=200, description="Titre du produit")
    description: Optional[str] = Field(None, description="Description facultative")
    price: Decimal = Field(..., ge=0, decimal_places=2, description="Prix en euros (>= 0)")
    stock: int = Field(0, ge=0, description="Quantité en stock")
    is_active: bool = Field(True, description="Produit actif ou masqué")
    category_id: Optional[UUID] = Field(None, description="ID de la catégorie (optionnel)")


class ProductCreate(ProductBase):
    """Données requises pour créer un produit."""
    pass


class ProductUpdate(BaseModel):
    """Données pour la mise à jour partielle (tous optionnels)."""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    category_id: Optional[UUID] = None

class ProductRead(ProductBase):
    """Données retournées au client (inclut ID )."""
    id: UUID


    class Config:
        from_attributes = True