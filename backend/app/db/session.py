from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from app.core.config import settings

# -----------------------------
# Async engine for FastAPI runtime
# -----------------------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # proactively tests connections from the pool
)

# Factory that gives you AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# FastAPI dependency you can "inject" into endpoint functions
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# -----------------------------
# Sync engine for Alembic (autogenerate migrations)
# -----------------------------
# Replace asyncpg driver with psycopg2 for sync use
sync_database_url = settings.DATABASE_URL.replace("asyncpg", "psycopg2")
engine.sync_engine = create_engine(sync_database_url, echo=True)