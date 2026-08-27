# controllers/product.py - Contrôleur des produits
from fastapi import BackgroundTasks
from schemas.product import ProductSearchParams
from services.product_service import ProductService


class ProductController:
    """
    Contrôleur pour les actions liées aux produits.
    Fait uniquement le lien entre la route et le service.
    Injecte les BackgroundTasks indispensables pour Meilisearch.
    """
    def __init__(self, db):
        self.db = db
        self.service = ProductService(db)

    def create_product(self, product_data: dict, background_tasks: BackgroundTasks):
        return self.service.create_product(product_data, background_tasks)

    def get_product_by_id(self, product_id: str):
        return self.service.get_product_by_id(product_id)

    def update_product(self, product_id: str, product_data: dict, background_tasks: BackgroundTasks):
        return self.service.update_product(product_id, product_data, background_tasks)

    def delete_product(self, product_id: str, background_tasks: BackgroundTasks):
        return self.service.delete_product(product_id, background_tasks)

    async def search_products(self, params: ProductSearchParams):
        # Transmet l'appel asynchrone directement au service Meilisearch
        return await self.service.search_products(params)
