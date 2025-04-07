from typing import Protocol

from secret_app.presentation.schemas import requests, responses


class CreateSecretControllerProtocol(Protocol):
    async def create_secret(
            self,
            create_request_data: requests.SecretPostRequest,
        ) -> responses.SecretPostResponse: ...


class GetSecretControllerProtocol(Protocol): ...


class DeleteSecretControllerProtocol(Protocol): ...

