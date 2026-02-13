import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DB_PATH = 'database.db'
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')


engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
