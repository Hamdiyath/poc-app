from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from models.product import Product
from schemas.product import ProductSearchParams
from utils.search import search_client, sync_product_to_search, delete_product_from_search
from fastapi import BackgroundTasks


# ... Conservez vos fonctions get_by_id et get_by_title intactes ...

# ---------- Le Nouveau Moteur de Recherche ----------
async def search_products(params: ProductSearchParams) -> Tuple[List[dict], int]:
    """
    Remplace l'ancienne recherche SQL. Interroge Meilisearch de manière asynchrone.
    Retourne (liste des hits au format dict, nombre total de résultats estimés).
    """
    index = search_client.index("products")

    # Construction dynamique des filtres Meilisearch
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
        filter_chunks.append(f"is_active = {str(params.is_active).lower()}")

    # Gestion du Tri
    sort_option = None
    if params.sort_by:
        # Correspondance pour le timestamp de création si demandé
        field = "created_at" if params.sort_by == "created_at" else params.sort_by
        sort_option = [f"{field}:{params.sort_order}"]

    # Requête de recherche facettée instantanée
    search_results = await index.search(
        query=params.search or "",
        filter=" AND ".join(filter_chunks) if filter_chunks else None,
        sort=sort_option,
        offset=params.skip,
        limit=params.limit
    )

    return search_results.hits, search_results.estimated_total_hits


# ---------- Création (Modifiée pour inclure la Synchro) ----------
def create(db: Session, product_data: dict, background_tasks: BackgroundTasks) -> Product:
    nouveau_produit = Product(**product_data)
    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)

    # Utilisation d'une tâche d'arrière-plan pour ne pas bloquer la réponse de l'API
    background_tasks.add_task(sync_product_to_search, nouveau_produit)
    return nouveau_produit


# ---------- Mise à jour (Modifiée pour inclure la Synchro) ----------
def update(db: Session, product_id: UUID, product_data: dict, background_tasks: BackgroundTasks) -> Optional[Product]:
    product = get_by_id(db, product_id)
    if not product:
        return None
    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)

    # Met à jour Meilisearch avec les nouvelles valeurs
    background_tasks.add_task(sync_product_to_search, product)
    return product


# ---------- Suppression (Modifiée pour inclure la Synchro) ----------
def delete(db: Session, product_id: UUID, background_tasks: BackgroundTasks) -> bool:
    product = get_by_id(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()

    # Supprime du moteur de recherche
    background_tasks.add_task(delete_product_from_search, str(product_id))
    return True
