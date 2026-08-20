
# config.py - Configuration de l'application


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # ---------- Configuration de l'API ----------
    app_name: str = "API Proof of Concept"
    app_description: str = "API de test de recherche et de filtrage dynamique des produits pour un site d'e-commerces"
    app_version: str = "1.0.0"
    debug: bool = False

    # ---------- Base de données ----------
    database_url: str = Field(..., description="URL de connexion à la base de données")

    # ---------- Configuration du fichier .env ----------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )





# ---------- Instance globale ----------
settings = Settings()
