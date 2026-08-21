# core/handlers.py - Gestionnaire global d'exceptions

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from exceptions.base import (
    AppError,
    ProductNotFoundError,
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
    InvalidPriceRangeError,
)


def setup_exception_handlers(app: FastAPI):
    """Configure les gestionnaires d'exceptions pour l'application."""

    @app.exception_handler(AppError)
    def app_error_handler(request: Request, exc: AppError):
        status_code = 400
        error_code = "BAD_REQUEST"

        # ---------- 404 Not Found ----------
        if isinstance(exc, (ProductNotFoundError, CategoryNotFoundError)):
            status_code = 404
            error_code = "NOT_FOUND"

        # ---------- 409 Conflict (Doublons) ----------
        elif isinstance(exc, CategoryAlreadyExistsError):
            status_code = 409
            error_code = "CONFLICT"

        # ---------- 400 Bad Request (Règles métier) ----------
        elif isinstance(exc, InvalidPriceRangeError):
            status_code = 400
            error_code = "BAD_REQUEST"

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": {
                    "error_code": error_code,
                    "type": exc.__class__.__name__
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    def validation_error_handler(request: Request, exc: RequestValidationError):
        first_err = exc.errors()[0]
        field = first_err.get("loc", [])[-1]
        msg = first_err.get("msg")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": f"Champ '{field}' invalide : {msg}",
                "data": None
            }
        )

    @app.exception_handler(Exception)
    def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Erreur interne du serveur",
                "data": None
            }
        )