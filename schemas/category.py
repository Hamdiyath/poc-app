from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Schéma de base contenant les champs communs."""
    name: str = Field(..., max_length=100, description="Nom de la catégorie")
    slug: str = Field(..., max_length=100, description="Slug unique pour l'URL")
    description: Optional[str] = Field(None, description="Description facultative")
    is_active: bool = Field(True, description="Catégorie active ou masquée")


class CategoryCreate(CategoryBase):
    """Schéma pour la création d'une catégorie (hérite de Base)."""
    pass


class CategoryUpdate(BaseModel):
    """Schéma pour la mise à jour partielle (tous les champs sont optionnels)."""
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryRead(CategoryBase):
    id: UUID
    created_at: datetime


    class Config:
        from_attributes = True  # Permet de convertir un objet SQLAlchemy en JSON