from dependency_injector import containers, providers

from core.security import Security
from core.uow import UnitOfWork
from secret_app.application.usecases.create_secret_usecase import CreateSecretUsecase
from secret_app.application.usecases.delete_secret_usecase import DeleteSecretUsecase
from secret_app.application.usecases.read_secret_usecase import ReadSecretUseCase


class ApplicationContainer(containers.DeclarativeContainer):
    """Application layer container for the secret application."""

    security: providers.Dependency[Security] = providers.Dependency(instance_of=Security)
    uow: providers.Dependency[UnitOfWork] = providers.Dependency(instance_of=UnitOfWork)


    create_secret_uc: providers.Factory[CreateSecretUsecase] = providers.Factory(
        CreateSecretUsecase,
        uow=uow,
        security=security,
    )
    delete_secret_uc: providers.Factory[DeleteSecretUsecase] = providers.Factory(
        DeleteSecretUsecase,
        uow=uow,
        security=security,
    )
    get_secret_uc: providers.Factory[ReadSecretUseCase] = providers.Factory(
        ReadSecretUseCase,
        uow=uow,
        security=security,
    )

