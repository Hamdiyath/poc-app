# repositories/product.py - Opérations de base de données pour Product
from typing import Optional, List, Tuple
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from models.product import Product


# ---------- Récupération par ID ----------
def get_by_id(db: Session, product_id: UUID) -> Optional[Product]:
    """Récupère un produit par son ID avec sa catégorie."""
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )


# ---------- Récupération par titre ----------
def get_by_title(db: Session, title: str) -> Optional[Product]:
    """Récupère un produit par son titre exact."""
    return db.query(Product).filter(Product.title == title).first()


# ---------- Recherche multi-critères (PostgreSQL) ----------
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
    """Recherche des produits en BDD selon plusieurs filtres optionnels."""
    query = db.query(Product).options(joinedload(Product.category))

    # Filtres
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))

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

    # Compte total avant pagination
    total = query.count()

    # Tri
    sort_columns = {
        "price": Product.price,
        "stock": Product.stock,
        "created_at": Product.created_at,
        "title": Product.title,
    }
    if sort_by in sort_columns:
        column = sort_columns[sort_by]
        query = query.order_by(column.desc() if sort_order == "desc" else column.asc())

    # Pagination
    products = query.offset(skip).limit(limit).all()

    return products, total


# ---------- Création ----------
def create(db: Session, product_data: dict) -> Product:
    """Crée un produit en base de données."""
    nouveau_produit = Product(**product_data)
    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)
    return nouveau_produit


# ---------- Mise à jour ----------
def update(db: Session, product_id: UUID, product_data: dict) -> Optional[Product]:
    """Met à jour un produit existant."""
    product = get_by_id(db, product_id)
    if not product:
        return None

    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# ---------- Suppression ----------
def delete(db: Session, product_id: UUID) -> bool:
    """Supprime un produit de la base de données."""
    product = get_by_id(db, product_id)
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True