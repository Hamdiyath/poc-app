# routes/products.py - Routes pour les produits (Version Optimisée Meilisearch)
from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductSearchParams
from controllers.product import ProductController
from schemas.response import ApiResponse, PaginatedData

router = APIRouter(prefix="/products", tags=["Products"])


# ---------- Recherche multi-critères (Le coeur du POC optimisé) ----------
# Note: On passe à 'async def' car l'appel à Meilisearch est asynchrone
@router.get("/", response_model=ApiResponse[PaginatedData[dict]])
async def search_products(params: ProductSearchParams = Depends(), db: Session = Depends(get_db)):
    controller = ProductController(db)
    # On passe l'objet de paramètres directement
    result = await controller.search_products(params)
    return ApiResponse(success=True, message="Produits récupérés avec succès", data=result)


# ---------- Récupérer un produit par ID ----------
@router.get("/{product_id}", response_model=ApiResponse[ProductRead])
def get_product_by_id_route(product_id: str, db: Session = Depends(get_db)):
    controller = ProductController(db)
    result = controller.get_product_by_id(product_id)
    return ApiResponse(success=True, message="Produit récupéré avec succès", data=result)


# ---------- Créer un produit ----------
@router.get("/", response_model=ApiResponse[PaginatedData[dict]])
async def search_products(params: ProductSearchParams = Depends(), db: Session = Depends(get_db)):
    controller = ProductController(db)
    hits, total = await controller.search_products(params)

    paginated_data = PaginatedData(
        items=hits,
        total=total,
        skip=params.skip,
        limit=params.limit
    )
    return ApiResponse(success=True, message="Produits récupérés avec succès", data=paginated_data)


# ---------- Modifier un produit ----------
@router.put("/{product_id}", response_model=ApiResponse[ProductRead])
def update_existing_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks() # Ajouté pour la synchro
):
    controller = ProductController(db)
    result = controller.update_product(product_id, product_data.model_dump(exclude_unset=True), background_tasks)
    return ApiResponse(success=True, message="Produit mis à jour avec succès", data=result)


# ---------- Supprimer un produit ----------
@router.delete("/{product_id}", response_model=ApiResponse[None])
def delete_existing_product(
    product_id: str,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks() # Ajouté pour la synchro
):
    controller = ProductController(db)
    controller.delete_product(product_id, background_tasks)
    return ApiResponse(success=True, message="Produit supprimé avec succès", data=None)
