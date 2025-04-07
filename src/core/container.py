from dependency_injector import containers, providers

from core.config import config
from core.database import DataBase
from core.security import Security
from core.uow import UnitOfWork
from secret_app.application.container import ApplicationContainer
from secret_app.presentation.container import PresentationContainer


class Container(containers.DeclarativeContainer):
    """Main application container."""

    wiring_config = containers.WiringConfiguration(packages=["api.v1"])

    security: providers.Singleton[Security] = providers.Singleton(
        Security,
        secret_key=config.sec_app.CRYPTO_KEY,
    )
    db: providers.Singleton[DataBase] = providers.Singleton(
        DataBase,
        dsn=config.db.dsn,
    )
    uow: providers.Singleton[UnitOfWork] = providers.Singleton(
        UnitOfWork,
        db=db,
    )

    application_container = providers.Container(
        ApplicationContainer,
        security=security,
        uow=uow,
    )

    presentation_container = providers.Container(
        PresentationContainer,
        application_container=application_container,
    )
