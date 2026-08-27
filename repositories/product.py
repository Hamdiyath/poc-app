from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductSearchParams
from utils.search import search_client, sync_product_to_search, delete_product_from_search
from fastapi import BackgroundTasks


# ---------- Fonctions utilitaires basiques ----------
def get_by_id(db: Session, product_id: UUID) -> Optional[Product]:
    """Récupère un produit par son ID."""
    return db.query(Product).filter(Product.id == product_id).first()


def get_by_title(db: Session, title: str) -> Optional[Product]:
    """Récupère un produit par son titre exact."""
    return db.query(Product).filter(Product.title == title).first()


# ---------- Le Moteur de Recherche Meilisearch ----------
async def search_products(params: ProductSearchParams) -> Tuple[List[dict], int]:
    """
    Interroge Meilisearch de manière asynchrone.
    Retourne (liste des hits au format dict, nombre total de résultats).
    """
    index = search_client.index("products")

    # 1. Construction dynamique des filtres Meilisearch
    filter_chunks = []
    if params.category_id:
        filter_chunks.append(f"category_id = '{params.category_id}'")
    if params.price_min is not None:
        filter_chunks.append(f"price >= {params.price_min}")
    if params.price_max is not None:
        filter_chunks.append(f"price <= {params.price_max}")
    if params.in_stock is True:
        filter_chunks.append("stock > 0")
    elif params.in_stock is False:
        filter_chunks.append("stock = 0")
    if params.is_active is not None:
        filter_chunks.append(f"is_active = {'true' if params.is_active else 'false'}")

    filter_query = " AND ".join(filter_chunks) if filter_chunks else None

    # 2. Gestion du Tri
    sort_option = None
    if getattr(params, "sort_by", None):
        field = "created_at" if params.sort_by == "created_at" else params.sort_by
        order = getattr(params, "sort_order", "asc")
        sort_option = [f"{field}:{order}"]

    # 3. Requête Meilisearch
    search_results = await index.search(
        query=params.search or "",
        filter=filter_query,
        sort=sort_option,
        offset=params.skip,
        limit=params.limit
    )

    total_count = getattr(search_results, "estimated_total_hits", getattr(search_results, "total_hits", 0))

    return search_results.hits, total_count


# ---------- Création (avec Synchro) ----------
def create(db: Session, product_data: dict, background_tasks: BackgroundTasks) -> Product:
    nouveau_produit = Product(**product_data)
    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)

    # Tâche d'arrière-plan pour ne pas bloquer la réponse API
    background_tasks.add_task(sync_product_to_search, nouveau_produit)
    return nouveau_produit


# ---------- Mise à jour (avec Synchro) ----------
def update(db: Session, product_id: UUID, product_data: dict, background_tasks: BackgroundTasks) -> Optional[Product]:
    product = get_by_id(db, product_id)
    if not product:
        return None

    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)

    db.commit()
    db.refresh(product)

    background_tasks.add_task(sync_product_to_search, product)
    return product


# ---------- Suppression (avec Synchro) ----------
def delete(db: Session, product_id: UUID, background_tasks: BackgroundTasks) -> bool:
    product = get_by_id(db, product_id)
    if not product:
        return False

    db.delete(product)
    db.commit()

    background_tasks.add_task(delete_product_from_search, str(product_id))
    return True