# crud/product_service.py - Opérations CRUD pour la table Product
from typing import Optional, List, Tuple
from uuid import UUID
from decimal import Decimal
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload
from models.product import Product


# ---------- Récupération par ID ----------
def get_by_id(db: Session, product_id: UUID) -> Optional[Product]:
    """
    Récupère un produit par son ID (UUID), avec sa catégorie chargée.
    """
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )


# ---------- Récupération par titre (recherche exacte) ----------
def get_by_title(db: Session, title: str) -> Optional[Product]:
    """
    Récupère un produit par son titre exact.
    """
    return db.query(Product).filter(Product.title == title).first()


# ---------- Recherche multi-critères ----------
def search_products(
        db: Session,
        search: Optional[str] = None,
        category_id: Optional[UUID] = None,
        price_min: Optional[Decimal] = None,
        price_max: Optional[Decimal] = None,
        in_stock: Optional[bool] = None,
        is_active: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        skip: int = 0,
        limit: int = 100,
) -> Tuple[List[Product], int]:
    """
    Recherche des produits selon une combinaison de filtres.
    Tous les filtres sont optionnels et combinables entre eux.
    Retourne (liste des produits, nombre total de résultats sans pagination).
    """
    query = db.query(Product).options(joinedload(Product.category))

    # ---------- Filtres appliqués conditionnellement ----------
    if search:
        # Combine ILIKE (correspondance exacte/sous-chaîne) et similarity (tolérance aux fautes)
        # 0.3 est le seuil de similarité recommandé (entre 0.0 et 1.0)
        query = query.filter(
            or_(
                Product.title.ilike(f"%{search}%"),
                func.similarity(Product.title, search) > 0.3
            )
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if price_min is not None:
        query = query.filter(Product.price >= price_min)

    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    if in_stock is True:
        query = query.filter(Product.stock > 0)
    elif in_stock is False:
        query = query.filter(Product.stock == 0)

    if is_active is not None:
        query = query.filter(Product.is_active == is_active)

    # ---------- Count total AVANT pagination ----------
    total = query.count()

    # ---------- Tri ----------
    sort_columns = {
        "price": Product.price,
        "stock": Product.stock,
        "created_at": Product.created_at,
        "title": Product.title,
    }

    if sort_by in sort_columns:
        column = sort_columns[sort_by]
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())
    elif search:
        # Tri par pertinence si aucun tri spécifique n'est demandé
        query = query.order_by(func.similarity(Product.title, search).desc())

    # ---------- Pagination ----------
    products = query.offset(skip).limit(limit).all()

    return products, total


# ---------- Création d'un produit ----------
def create(db: Session, product_data: dict) -> Product:
    """
    Crée un nouveau produit.
    """
    nouveau_produit = Product(**product_data)
    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)
    return nouveau_produit


# ---------- Mise à jour d'un produit ----------
def update(db: Session, product_id: UUID, product_data: dict) -> Optional[Product]:
    """
    Met à jour un produit existant.
    """
    product = get_by_id(db, product_id)
    if not product:
        return None
    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


# ---------- Suppression d'un produit ----------
def delete(db: Session, product_id: UUID) -> bool:
    """
    Supprime un produit.
    """
    product = get_by_id(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True