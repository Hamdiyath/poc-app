import os
from meilisearch_python_async import Client
from models.product import Product

search_client = Client(
    url="https://ms-aa0da662e565-53588.par.meilisearch.io",
    api_key="0fee97302d940747eb5ba148dcc276c4b65cf12477bb9ae703591f1204cf76e9"
)


# ... Conservez le reste du fichier (sync_product_to_search, etc.) identique ...


async def sync_product_to_search(product: Product):
    """Envoie ou met à jour un produit dans Meilisearch."""
    index = search_client.index("products")
    await index.add_documents([{
        "id": str(product.id),
        "title": product.title,
        "description": product.description,
        "price": float(product.price), # Meilisearch attend un float, pas un Decimal
        "stock": product.stock,
        "category_id": str(product.category_id) if product.category_id else None,
        "is_active": product.is_active,
        "created_at": int(product.created_at.timestamp()) # Utile pour trier par nouveauté
    }])

async def delete_product_from_search(product_id: str):
    """Supprime un produit de Meilisearch."""
    index = search_client.index("products")
    await index.delete_document(product_id)
