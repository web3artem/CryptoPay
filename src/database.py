from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from config import settings

DATABASE_URL = settings.ASYNC_DATABASE_URL

async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

sync_engine = create_engine(settings.SYNC_DATABASE_URL)
sync_session_maker = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_sync_session() -> Generator[Session, None, None]:
    session = sync_session_maker()
    try:
        yield session
    finally:
        session.close()
