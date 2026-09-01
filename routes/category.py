# routes/categories.py - Routes pour les catégories
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.category import CategorySearchParams

from database import get_db
from schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from controllers.category import CategoryController
from schemas.pagination import PaginatedData
from schemas.response import ApiResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


# ---------- Créer une catégorie ----------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[CategoryRead])
def create_new_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle catégorie."""
    controller = CategoryController(db)
    result = controller.create_category(category_data.model_dump())
    return ApiResponse(success=True, message="Catégorie créée avec succès", data=result)


# ---------- Lister toutes les catégories ----------
@router.get("/", response_model=ApiResponse[PaginatedData[CategoryRead]])
def get_all_categories(params: CategorySearchParams = Depends(), db: Session = Depends(get_db)):
    """Récupérer toutes les catégories (paginé)."""
    controller = CategoryController(db)
    result = controller.get_all_categories(params)
    return ApiResponse(success=True, message="Catégories récupérées avec succès", data=result)


# ---------- Récupérer une catégorie par ID ----------
@router.get("/{category_id}", response_model=ApiResponse[CategoryRead])
def get_category_by_id_route(category_id: str, db: Session = Depends(get_db)):
    """Récupérer une catégorie par son ID."""
    controller = CategoryController(db)
    result = controller.get_category_by_id(category_id)
    return ApiResponse(success=True, message="Catégorie récupérée avec succès", data=result)


# ---------- Modifier une catégorie ----------
@router.put("/{category_id}", response_model=ApiResponse[CategoryRead])
def update_existing_category(category_id: str, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    """Modifier une catégorie existante."""
    controller = CategoryController(db)
    result = controller.update_category(category_id, category_data.model_dump(exclude_unset=True))
    return ApiResponse(success=True, message="Catégorie mise à jour avec succès", data=result)


# ---------- Supprimer une catégorie ----------
@router.delete("/{category_id}", response_model=ApiResponse[None])
def delete_existing_category(category_id: str, db: Session = Depends(get_db)):
    """Supprimer une catégorie."""
    controller = CategoryController(db)
    controller.delete_category(category_id)
    return ApiResponse(success=True, message="Catégorie supprimée avec succès", data=None)