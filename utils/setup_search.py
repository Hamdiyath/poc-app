# setup_search.py - Initialisation de l'index Meilisearch Cloud
import asyncio
import os
from dotenv import load_dotenv
from meilisearch_python_async import Client

# Charger les variables du fichier .env
load_dotenv()


async def initialize_meilisearch():
    url = os.getenv("MEILISEARCH_URL")
    master_key = os.getenv("MEILISEARCH_MASTER_KEY")

    if not url or not master_key:
        print("❌ Erreur : MEILISEARCH_URL ou MEILISEARCH_MASTER_KEY manquant dans le .env")
        return

    print("🛰️ Connexion à Meilisearch Cloud...")
    async with Client(url=url, api_key=master_key) as client:
        # 1. Définition et création de l'index
        index_uid = "products"
        print(f"📦 Configuration de l'index '{index_uid}'...")
        index = client.index(index_uid)

        # 2. Définir les attributs filtrables (indispensable pour votre filtrage dynamique)
        # Ce sont les champs présents dans vos requêtes WHERE
        filterable_attributes = [
            "category_id",
            "price",
            "stock",
            "is_active"
        ]
        await index.update_filterable_attributes(filterable_attributes)
        print("✅ Attributs filtrables configurés.")

        # 3. Définir les attributs triables (indispensable pour vos tris dynamiques)
        # Ce sont les champs présents dans vos clauses ORDER BY
        sortable_attributes = [
            "price",
            "stock",
            "created_at",
            "title"
        ]
        await index.update_sortable_attributes(sortable_attributes)
        print("✅ Attributs triables configurés.")

        print("\n🚀 L'index Meilisearch Cloud est correctement configuré et prêt à l'emploi !")


if __name__ == "__main__":
    asyncio.run(initialize_meilisearch())
