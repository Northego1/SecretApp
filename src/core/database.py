from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class DataBase:
    def __init__(self: Self, dsn: str) -> None:
        self.engine = create_async_engine(url=dsn)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    # @asynccontextmanager
    # async def connection(self: Self) -> AsyncGenerator[AsyncConnection, None]:
    #     async with self.engine.begin() as conn:
    #         yield conn


    async def session_maker(self: Self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


class Base(DeclarativeBase):
    pass
