from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine
from app.core.config import settings
from app.models.base import Base

# Import models so metadata is populated for autogenerate:
from app.models import user  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def _sync_url(url: str) -> str:
    # Alembic runs synchronously; swap async driver for a sync one.
    # e.g. "postgresql+asyncpg://..." -> "postgresql+psycopg://..."
    return url.replace("+asyncpg", "+psycopg")

def run_migrations_online():
    sync_url = _sync_url(settings.DATABASE_URL)
    engine = create_engine(sync_url, pool_pre_ping=True)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
