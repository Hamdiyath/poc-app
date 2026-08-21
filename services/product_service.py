# service/product_service.py - Logique métier pour Product
from typing import Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from repositories import product as product_crud
from repositories import category as category_crud
from exceptions.base import ProductNotFoundError, CategoryNotFoundError, InvalidPriceRangeError
from schemas.response import PaginatedData


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Recherche multi-critères ----------
    def search_products(
        self,
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
    ) -> PaginatedData:

        if price_min is not None and price_max is not None and price_min > price_max:
            raise InvalidPriceRangeError()

        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)

        products, total = product_crud.search_products(
            self.db,
            search=search,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
            in_stock=in_stock,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
        )

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