from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=15
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_async_session():
    async with async_session() as session:
        yield session