# crud/category_service.py - Opérations CRUD pour la table Category

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from models.category import Category


# ---------- Récupération par ID ----------
#traduction exacte de cette route et de chaque route
def get_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    """
    Récupère une catégorie par son ID (UUID).
    """
    return db.query(Category).filter(Category.id == category_id).first()


# ---------- Récupération par slug ----------
def get_by_slug(db: Session, slug: str) -> Optional[Category]:
    """
    Récupère une catégorie par son slug.
    """
    return db.query(Category).filter(Category.slug == slug).first()


# ---------- Récupération par nom ----------
def get_by_name(db: Session, name: str) -> Optional[Category]:
    """
    Récupère une catégorie par son nom.
    """
    return db.query(Category).filter(Category.name == name).first()


# ---------- Récupération de toutes les catégories ----------
def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    """
    Récupère une liste paginée de catégories.
    """
    return db.query(Category).offset(skip).limit(limit).all()

# ---------- Comptage total ----------
def count_all(db: Session) -> int:
    """
    Compte le nombre total de catégories.
    """
    return db.query(Category).count()


# ---------- Création d'une catégorie ----------
def create(db: Session, category_data: dict) -> Category:
    """
    Crée une nouvelle catégorie.
    """
    nouvelle_categorie = Category(**category_data)
    db.add(nouvelle_categorie)
    db.commit()
    db.refresh(nouvelle_categorie)
    return nouvelle_categorie


# ---------- Mise à jour d'une catégorie ----------
def update(db: Session, category_id: UUID, category_data: dict) -> Optional[Category]:
    """
    Met à jour une catégorie existante.
    """
    category = get_by_id(db, category_id)
    if not category:
        return None

    for key, value in category_data.items():
        if value is not None:
            setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


# ---------- Suppression d'une catégorie ----------
def delete(db: Session, category_id: UUID) -> bool:
    """
    Supprime une catégorie.
    """
    category = get_by_id(db, category_id)
    if not category:
        return False

    db.delete(category)
    db.commit()
    return True


