# controllers/product.py - Contrôleur des produits
from services.product_service import ProductService
from schemas.product import ProductSearchParams

class ProductController:
    """
    Contrôleur pour les actions liées aux produits.
    Fait le lien entre la route et le service.
    Ne contient aucune logique métier.
    """
    def __init__(self, db):
        self.db = db
        self.service = ProductService(db)

    def create_product(self, product_data):
        return self.service.create_product(product_data)

    def get_product_by_id(self, product_id):
        return self.service.get_product_by_id(product_id)

    def update_product(self, product_id, product_data):
        return self.service.update_product(product_id, product_data)

    def delete_product(self, product_id):
        return self.service.delete_product(product_id)

    # controller
    def search_products(self, params: ProductSearchParams):
        # Transmets l'objet params directement au service (identique à CategoryController)
        return self.service.search_products(params)