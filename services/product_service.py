# services/product_service.py - Logique métier pour Product
from math import ceil
from uuid import UUID
from sqlalchemy.orm import Session
from repositories import product as product_crud
from repositories import category as category_crud
from exceptions.base import ProductNotFoundError, CategoryNotFoundError, InvalidPriceRangeError
from schemas.pagination import PaginatedData , create_paginated_response
from schemas.product import ProductSearchParams


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Recherche multi-critères avec pagination ----------
    def search_products(self, params: ProductSearchParams):
        # 1. Validation métier
        if params.price_min is not None and params.price_max is not None and params.price_min > params.price_max:
            raise InvalidPriceRangeError()

        if params.category_id is not None:
            if not category_crud.get_by_id(self.db, params.category_id):
                raise CategoryNotFoundError(params.category_id)

        # 2. Calcul du pas (skip)
        skip = (params.page - 1) * params.limit

        # 3. Conversion de params en dictionnaire pour les filtres du CRUD/Repository
        filters = params.model_dump(exclude={"page", "limit"}, exclude_none=True)

        # ---------- Pagination ----------
        skip = (params.page - 1) * params.limit
        items, total = product_crud.search_products(self.db, skip=skip, limit=params.limit, **filters)

        # 4. Construction de la réponse sans aucun calcul manuel dans le service
        return create_paginated_response(items=items,total=total,page=params.page,limit=params.limit)

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