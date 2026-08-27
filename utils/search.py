import os
from dotenv import load_dotenv # Import ajouté
from meilisearch_python_async import Client
from models.product import Product

# On charge le .env pour être sûr que l'API lit vos identifiants Cloud
load_dotenv()

search_client = Client(
    url=os.getenv("MEILISEARCH_URL"),
    api_key=os.getenv("MEILISEARCH_MASTER_KEY")
)


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
