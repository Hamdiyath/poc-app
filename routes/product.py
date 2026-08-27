# routes/products.py - Routes pour les produits
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from database import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductRead ,ProductSearchParams
from controllers.product import ProductController
from schemas.response import ApiResponse, PaginatedData

router = APIRouter(prefix="/products", tags=["Products"])


# ---------- Recherche multi-critères (le coeur du POC) ----------
@router.get("/", response_model=ApiResponse[PaginatedData[ProductRead]])
def search_products(params: ProductSearchParams = Depends(),db: Session = Depends(get_db)):
    controller = ProductController(db)
    result = controller.search_products(**params.model_dump())
    return ApiResponse(success=True, message="Produits récupérés avec succès", data=result)

# ---------- Récupérer un produit par ID ----------
@router.get("/{product_id}", response_model=ApiResponse[ProductRead])
def get_product_by_id_route(product_id: str, db: Session = Depends(get_db)):
    """Récupérer un produit par son ID."""
    controller = ProductController(db)
    result = controller.get_product_by_id(product_id)
    return ApiResponse(success=True, message="Produit récupéré avec succès", data=result)


# ---------- Créer un produit ----------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[ProductRead])
def create_new_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Créer un nouveau produit."""
    controller = ProductController(db)
    result = controller.create_product(product_data.model_dump())
    return ApiResponse(success=True, message="Produit créé avec succès", data=result)


# ---------- Modifier un produit ----------
@router.put("/{product_id}", response_model=ApiResponse[ProductRead])
def update_existing_product(product_id: str, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """Modifier un produit existant."""
    controller = ProductController(db)
    result = controller.update_product(product_id, product_data.model_dump(exclude_unset=True))
    return ApiResponse(success=True, message="Produit mis à jour avec succès", data=result)


# ---------- Supprimer un produit ----------
@router.delete("/{product_id}", response_model=ApiResponse[None])
def delete_existing_product(product_id: str, db: Session = Depends(get_db)):
    """Supprimer un produit."""
    controller = ProductController(db)
    controller.delete_product(product_id)
    return ApiResponse(success=True, message="Produit sufrom typing import Optionalpprimé avec succès", data=None)