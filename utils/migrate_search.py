# migrate_to_search.py - Migration de PostgreSQL (Neon) vers Meilisearch Cloud
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Importation de vos configurations locales
from database import SessionLocal  # Assurez-vous que c'est le bon nom dans votre database.py
from models.product import Product
from utils.search import sync_product_to_search

# Charger les variables d'environnement
load_dotenv()


async def migrate_products():
    print("🔌 Connexion à la base de données PostgreSQL (Neon)...")
    db: Session = SessionLocal()

    try:
        # 1. Récupérer tous les produits de la base de données
        products = db.query(Product).all()
        total_products = len(products)

        if total_products == 0:
            print("ℹ️ Aucun produit trouvé dans PostgreSQL (Neon). La base est vide.")
            return

        print(f"📦 {total_products} produits trouvés. Début de l'indexation sur Meilisearch Cloud...")

        # 2. Boucler sur les produits et les envoyer vers Meilisearch
        for index, product in enumerate(products, start=1):
            await sync_product_to_search(product)
            print(f" 🔄 [{index}/{total_products}] Indexé : {product.title}")

        print("\n🚀 Migration terminée avec succès ! Tous vos produits sont disponibles à la recherche.")

    except Exception as e:
        print(f"❌ Une erreur est survenue lors de la migration : {str(e)}")

    finally:
        db.close()
        print("🔌 Connexion PostgreSQL fermée.")


if __name__ == "__main__":
    asyncio.run(migrate_products())
