from typing import Optional
from decimal import Decimal
from uuid import UUID
from datetime import datetime

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


# Mettez à jour uniquement cette classe dans votre fichier schemas
class ProductSearchParams(BaseModel):
    search: Optional[str] = Field(None, description="Recherche textuelle")
    category_id: Optional[UUID] = Field(None, description="Filtrer par catégorie")
    price_min: Optional[Decimal] = Field(None, ge=0, description="Prix minimum")
    price_max: Optional[Decimal] = Field(None, ge=0, description="Prix maximum")
    in_stock: Optional[bool] = Field(None, description="En stock ou rupture")
    is_active: Optional[bool] = Field(True, description="Par défaut, uniquement les produits en ligne")
    sort_by: Optional[str] = Field(None, description="Tri : price, stock, title, created_at")
    sort_order: Optional[str] = Field("asc", description="asc ou desc")
    page: int = Field(1, ge=1, description="Numéro de la page")
    limit: int = Field(5, ge=1, le=100, description="Nombre d'éléments par page")


class ProductRead(ProductBase):
    """Données retournées au client (inclut ID)."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryNested] = None

    class Config:
        from_attributes = True

    class CategoryNested(BaseModel):
        """Version allégée de Category, imbriquée dans ProductRead."""
        id: UUID
        name: str
        slug: str

        class Config:
            from_attributes = True


