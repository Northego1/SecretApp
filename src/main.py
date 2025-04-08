from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncGenerator

import uvicorn
from fastapi import FastAPI

from api.v1 import union_router
from core.container import Container
from core.logger import get_logger

if TYPE_CHECKING:
    from core.redis import RedisClient

log = get_logger(__name__)

@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis_client: RedisClient = app.state.container.redis_client()
    await redis_client.connect()
    yield
    await redis_client.disconnect()


def create_app() -> FastAPI:
    """Create a FastAPI application instance."""
    log.debug("creating fastapi app")
    app = FastAPI(title="SecretApp", lifespan=_lifespan)
    app.include_router(union_router)

    log.debug("initing dependency container")
    container = Container()
    container.init_resources()  # type: ignore
    app.state.container = container
    return app


app = create_app()


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
