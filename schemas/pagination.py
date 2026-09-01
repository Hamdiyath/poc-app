from typing import Generic, TypeVar, List , Sequence
from math import ceil
from pydantic import BaseModel

T = TypeVar('T')

class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int
    hasNext: bool
    hasPrev: bool

class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationMeta


# ---------- Fonction centralisée ----------
def create_paginated_response(items: Sequence[T], total: int, page: int, limit: int) -> PaginatedData[T]:
    total_pages = ceil(total / limit) if total > 0 else 1

    return PaginatedData(
        items=list(items),
        pagination=PaginationMeta(
            total=total,
            page=page,
            limit=limit,
            totalPages=total_pages,
            hasNext=page < total_pages,
            hasPrev=page > 1
        )
    )