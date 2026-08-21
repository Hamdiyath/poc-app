# exceptions/base.py - Exceptions métier personnalisées

# Ces exceptions sont levées par les services.
# Elles sont interceptées par le gestionnaire global dans handlers.py
# et transformées en réponses HTTP.


class AppError(Exception):
    """
    Classe de base pour toutes les erreurs métier de l'application.
    Toutes les exceptions métier doivent hériter de cette classe.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


# ---------- Produits ----------
class ProductNotFoundError(AppError):
    """Levée quand un produit n'est pas trouvé."""
    def __init__(self, product_id=None):
        message = f"Produit '{product_id}' non trouvé" if product_id else "Produit non trouvé"
        super().__init__(message)


# ---------- Catégories ----------
class CategoryNotFoundError(AppError):
    """Levée quand une catégorie n'est pas trouvée."""
    def __init__(self, category_id=None):
        message = f"Catégorie '{category_id}' non trouvée" if category_id else "Catégorie non trouvée"
        super().__init__(message)


class CategoryAlreadyExistsError(AppError):
    """Levée quand une catégorie avec ce nom ou ce slug existe déjà."""
    def __init__(self, message: str = "Une catégorie avec ce nom ou ce slug existe déjà"):
        self.message = message
        super().__init__(self.message)


# ---------- Validation métier ----------
class InvalidPriceRangeError(AppError):
    """Levée quand price_min est supérieur à price_max."""
    def __init__(self):
        super().__init__("Le prix minimum ne peut pas être supérieur au prix maximum")