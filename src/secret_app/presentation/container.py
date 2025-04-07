from dependency_injector import containers, providers

from secret_app.presentation.controllers.create_secret_controller import CreateSecretController
from secret_app.presentation.controllers.delete_secret_controller import DeleteSecretController
from secret_app.presentation.controllers.get_secret_controller import GetSecretController


class PresentationContainer(containers.DeclarativeContainer):
    """Presentation layer container for the secret application."""

    application_container = providers.DependenciesContainer()

    create_secret_cl: providers.Factory[CreateSecretController] = providers.Factory(
        CreateSecretController,
        application_container.create_secret_uc, # type: ignore
    )

    get_secret_cl: providers.Factory[GetSecretController] = providers.Factory(
        GetSecretController,
        application_container.get_secret_uc, # type: ignore
    )

    delete_secret_cl: providers.Factory[DeleteSecretController] = providers.Factory(
        DeleteSecretController,
        application_container.delete_secret_uc, # type: ignore
    )
