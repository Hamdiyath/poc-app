# service/category_service.py - Logique métier pour Category
from uuid import UUID
from sqlalchemy.orm import Session
from repositories import category as category_crud
from exceptions.base import CategoryNotFoundError, CategoryAlreadyExistsError
from schemas.pagination import PaginatedData , create_paginated_response
from schemas.category import CategoryRead , CategorySearchParams


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Récupération d'une catégorie ----------
    def get_category_by_id(self, category_id: UUID) -> CategoryRead:
        category = category_crud.get_by_id(self.db, category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        return category

    # ---------- Liste paginée ----------
    def get_all_categories(self, params: CategorySearchParams) -> PaginatedData:
        # Récupération de l'offset à partir des attributs de l'objet params
        skip = (params.page - 1) * params.limit

        # Appel de la base de données
        categories, total = category_crud.get_paginated_categories(self.db,skip=skip,limit=params.limit)
        # helper centralisé
        return create_paginated_response(items=categories,total=total,page=params.page,limit=params.limit)


    # ---------- Création ----------
    def create_category(self, category_data: dict) -> CategoryRead:
        if category_crud.get_by_name(self.db, category_data["name"]):
            raise CategoryAlreadyExistsError()
        if category_crud.get_by_slug(self.db, category_data["slug"]):
            raise CategoryAlreadyExistsError()
        return category_crud.create(self.db, category_data)

    # ---------- Mise à jour ----------
    def update_category(self, category_id: UUID, category_data: dict) -> CategoryRead:
        existing = category_crud.get_by_id(self.db, category_id)
        if not existing:
            raise CategoryNotFoundError(category_id)

        new_name = category_data.get("name")
        if new_name and new_name != existing.name:
            if category_crud.get_by_name(self.db, new_name):
                raise CategoryAlreadyExistsError()

        new_slug = category_data.get("slug")
        if new_slug and new_slug != existing.slug:
            if category_crud.get_by_slug(self.db, new_slug):
                raise CategoryAlreadyExistsError()

        return category_crud.update(self.db, category_id, category_data)

    # ---------- Suppression ----------
    def delete_category(self, category_id: UUID) -> bool:
        existing = category_crud.get_by_id(self.db, category_id)
        if not existing:
            raise CategoryNotFoundError(category_id)
        return category_crud.delete(self.db, category_id)