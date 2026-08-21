# schemas/response.py - Schémas génériques réutilisables

from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedData(BaseModel, Generic[T]):
    """Enveloppe générique pour toute liste paginée."""
    items: List[T]
    total: int
    skip: int
    limit: int


class ApiResponse(BaseModel, Generic[T]):
    """Enveloppe générique pour toute réponse de succès."""
    success: bool = True
    message: str
    data: T