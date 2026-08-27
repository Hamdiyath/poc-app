# services/product_service.py - Logique métier pour Product

from uuid import UUID
from sqlalchemy.orm import Session
from repositories import product as product_crud
from repositories import category as category_crud
from exceptions.base import ProductNotFoundError, CategoryNotFoundError, InvalidPriceRangeError
from schemas.response import PaginatedData


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Recherche multi-critères ----------
    def search_products(self, **filters):
        price_min = filters.get("price_min")
        price_max = filters.get("price_max")
        category_id = filters.get("category_id")

        if price_min is not None and price_max is not None and price_min > price_max:
            raise InvalidPriceRangeError()

        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)

        products, total = product_crud.search_products(self.db, **filters)

        # .get() sécurisé avec valeurs par défaut au cas où 'skip' ou 'limit' sont absents
        skip = filters.get("skip", 0)
        limit = filters.get("limit", 100)

        return PaginatedData(items=products, total=total, skip=skip, limit=limit)

    # ---------- Récupération d'un produit ----------
    def get_product_by_id(self, product_id: UUID):
        product = product_crud.get_by_id(self.db, product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    # ---------- Création ----------
    def create_product(self, product_data: dict):
        category_id = product_data.get("category_id")
        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)
        return product_crud.create(self.db, product_data)

    # ---------- Mise à jour ----------
    def update_product(self, product_id: UUID, product_data: dict):
        existing = product_crud.get_by_id(self.db, product_id)
        if not existing:
            raise ProductNotFoundError(product_id)

        category_id = product_data.get("category_id")
        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)

        return product_crud.update(self.db, product_id, product_data)

    # ---------- Suppression ----------
    def delete_product(self, product_id: UUID) -> bool:
        existing = product_crud.get_by_id(self.db, product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        return product_crud.delete(self.db, product_id)