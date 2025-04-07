import uuid
from typing import Protocol

from fastapi import Response

from secret_app.presentation.schemas import requests, responses


class CreateSecretControllerProtocol(Protocol):
    async def create_secret(
        self,
        create_request_data: requests.SecretPostRequest,
    ) -> responses.SecretPostResponse: ...


class GetSecretControllerProtocol(Protocol):
    async def get_secret(
        self,
        secret_id: uuid.UUID,
        response: Response,
    ) -> responses.SecretGetReponse: ...


class DeleteSecretControllerProtocol(Protocol):
    async def delete_secret(
        self,
        secret_id: uuid.UUID,
        requested_data: requests.SecretDeleteRequest,
    ) -> None: ...
