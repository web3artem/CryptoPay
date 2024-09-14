from typing import AsyncGenerator, Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from config import settings

DATABASE_URL = settings.ASYNC_DATABASE_URL

_async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
_async_session_maker = async_sessionmaker(_async_engine, expire_on_commit=False)

_sync_engine = create_engine(settings.SYNC_DATABASE_URL)
_sync_session_maker = sessionmaker(bind=_sync_engine)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        yield session


@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    session = _sync_session_maker()
    try:
        yield session
    finally:
        session.close()
