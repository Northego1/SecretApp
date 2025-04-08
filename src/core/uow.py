import contextlib
import dataclasses
from typing import AsyncGenerator, Self

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import DataBase
from core.exceptions import AppError
from core.logger import get_logger
from core.redis import RedisClient
from secret_app.infrastructure.repository.secret_logs_repository import SecretLogRepository
from secret_app.infrastructure.repository.secret_repository import SecretRepository

log = get_logger(__name__)


@dataclasses.dataclass(slots=True)
class Repository:
    _conn: AsyncSession
    _redis: Redis

    _secret_repository: SecretRepository | None = None
    _secret_log_repository: SecretLogRepository | None = None

    @property
    def secret_repository(self: Self) -> SecretRepository:
        if self._secret_repository is None:
            self._secret_repository = SecretRepository(self._conn, self._redis)
        return self._secret_repository

    @property
    def secret_log_repository(self: Self) -> SecretLogRepository:
        if self._secret_log_repository is None:
            self._secret_log_repository = SecretLogRepository(self._conn)
        return self._secret_log_repository


class UnitOfWork:
    def __init__(self, db: DataBase, redis_client: RedisClient) -> None:
        self.db = db
        self.redis_client = redis_client

    @contextlib.asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[Repository, None]:
        async for session in self.db.session_maker():
            await session.begin()
            try:
                yield Repository(session, self.redis_client.redis)
                log.debug("Commiting transaction")
                await session.commit()
            except AppError as e:
                log.exception(
                    "AppError during transaction: %s, rollback",
                    e.detail,
                )
                await session.rollback()
                raise e from e
            except Exception as e:
                log.critical(
                    "Unexpected error during transaction: %s, rollback",
                    e,
                    exc_info=True,
                )
                await session.rollback()
                raise AppError from e
