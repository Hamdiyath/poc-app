# service/product_service.py - Logique métier pour Product
from typing import Optional
from uuid import UUID
from decimal import Decimal
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

# Importation de vos composants existants
from repositories import product as product_crud
from repositories import category as category_crud
from exceptions.base import ProductNotFoundError, CategoryNotFoundError, InvalidPriceRangeError
from schemas.response import PaginatedData
from schemas.product import ProductSearchParams


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Recherche multi-critères (Meilisearch Asynchrone) ----------
    async def search_products(self, params: ProductSearchParams) -> PaginatedData:
        """
        Effectue une recherche et un filtrage dynamique ultra-rapide via Meilisearch.
        Gère les validations métiers avant de lancer la requête.
        """
        # Validation métier : plage de prix cohérente
        if params.price_min is not None and params.price_max is not None and params.price_min > params.price_max:
            raise InvalidPriceRangeError()

        # Validation métier : vérification de l'existence de la catégorie dans PostgreSQL (Neon)
        if params.category_id is not None:
            if not category_crud.get_by_id(self.db, params.category_id):
                raise CategoryNotFoundError(params.category_id)

        # Appel asynchrone au repository mis à jour (Meilisearch)
        products, total = await product_crud.search_products(params)

        # Retourne les résultats enveloppés proprement dans votre structure PaginatedData
        return PaginatedData(
            items=products,
            total=total,
            skip=params.skip,
            limit=params.limit
        )

    # ---------- Récupération d'un produit (PostgreSQL - String vers UUID) ----------
    def get_product_by_id(self, product_id: str):
        try:
            uuid_obj = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'UUID invalide")

        product = product_crud.get_by_id(self.db, uuid_obj)
        if not product:
            raise ProductNotFoundError(uuid_obj)
        return product

    # ---------- Création (PostgreSQL + Tâche de fond Meilisearch) ----------
    def create_product(self, product_data: dict, background_tasks: BackgroundTasks):
        category_id = product_data.get("category_id")
        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)

        return product_crud.create(self.db, product_data, background_tasks)

    # ---------- Mise à jour (PostgreSQL + Tâche de fond Meilisearch) ----------
    def update_product(self, product_id: str, product_data: dict, background_tasks: BackgroundTasks):
        try:
            uuid_obj = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'UUID invalide")

        existing = product_crud.get_by_id(self.db, uuid_obj)
        if not existing:
            raise ProductNotFoundError(uuid_obj)

        category_id = product_data.get("category_id")
        if category_id is not None:
            if not category_crud.get_by_id(self.db, category_id):
                raise CategoryNotFoundError(category_id)

        return product_crud.update(self.db, uuid_obj, product_data, background_tasks)

    # ---------- Suppression (PostgreSQL + Tâche de fond Meilisearch) ----------
    def delete_product(self, product_id: str, background_tasks: BackgroundTasks) -> bool:
        try:
            uuid_obj = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'UUID invalide")

        existing = product_crud.get_by_id(self.db, uuid_obj)
        if not existing:
            raise ProductNotFoundError(uuid_obj)

        return product_crud.delete(self.db, uuid_obj, background_tasks)
