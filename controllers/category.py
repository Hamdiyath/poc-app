# controllers/category_service.py - Contrôleur des catégories
from services.category_service import CategoryService
from schemas.category import CategorySearchParams


class CategoryController:
    """
    Contrôleur pour les actions liées aux catégories.
    Fait le lien entre la route et le service.
    Ne contient aucune logique métier.
    """
    def __init__(self, db):
        self.db = db
        self.service = CategoryService(db)

    def create_category(self, category_data):
        return self.service.create_category(category_data)

    def get_category_by_id(self, category_id):
        return self.service.get_category_by_id(category_id)

    def update_category(self, category_id, category_data):
        return self.service.update_category(category_id, category_data)

    def delete_category(self, category_id):
        return self.service.delete_category(category_id)

    # ---------- Liste paginée ----------
    def get_all_categories(self, params: CategorySearchParams):
        return self.service.get_all_categories(params)