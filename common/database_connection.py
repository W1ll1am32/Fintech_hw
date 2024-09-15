from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from os import environ

DB = environ.get('DB')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')

DATABASE_URL = f"postgresql+asyncpg://{DB}:{DB}@{DB_HOST}:{DB_PORT}/{DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
