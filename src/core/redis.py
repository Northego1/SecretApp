from redis.asyncio import Redis

from core.logger import get_logger

log = get_logger(__name__)

class RedisClient:
    def __init__(
            self,
            redis_dsn: str,
    ) -> None:
        self._redis_dsn = redis_dsn
        self.redis: Redis | None = None


    async def connect(self) -> None:
        """Connect to the Redis server."""
        log.debug("Connecting to Redis server at %s", self._redis_dsn)
        self.redis = await Redis.from_url(self._redis_dsn) # type: ignore
        await self.redis.ping() # type: ignore
        log.debug("Connected to Redis server")


    async def disconnect(self) -> None:
        """Disconnect from the Redis server."""
        if self.redis:
            log.debug("Disconnecting from Redis server")
            await self.redis.close() # type: ignore
