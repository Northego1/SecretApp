import uvicorn
from fastapi import FastAPI

from api.v1 import union_router
from core.container import Container
from core.logger import get_logger

log = get_logger(__name__)


def create_app() -> FastAPI:
    """Create a FastAPI application instance."""
    log.debug("creating fastapi app")
    app = FastAPI()
    app.include_router(union_router)

    log.debug("initing dependency container")
    container = Container()
    container.init_resources() # type: ignore

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

