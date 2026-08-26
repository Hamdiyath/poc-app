"""add pg_trgm extension and gin index on product title

Revision ID: 9c91e3bac46b
Revises: 4f233f71c06b
Create Date: 2026-08-26 22:55:36.353041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c91e3bac46b'
down_revision: Union[str, Sequence[str], None] = '4f233f71c06b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Activation de l'extension trigramme dans PostgreSQL
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # 2. Création de l'index GIN spécial trigrammes sur le titre
    op.execute("CREATE INDEX idx_products_title_trgm ON products USING gin (title gin_trgm_ops);")


def downgrade() -> None:
    # Suppression de l'index et de l'extension si rollback
    op.execute("DROP INDEX IF EXISTS idx_products_title_trgm;")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")