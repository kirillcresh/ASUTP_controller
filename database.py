from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


async def get_session():
    engine = create_async_engine(
        DATABASE_URL, echo=True, future=True, pool_size=100, max_overflow=0
    )
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session()


Base = declarative_base()
metadata = MetaData(schema="public")
