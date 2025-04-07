from typing import Protocol

from fastapi import HTTPException

from core.exceptions import AppError
from secret_app.application.dto import CreateSecretDto
from secret_app.presentation.schemas import requests, responses


class CreateSecretUsecaseProtocol(Protocol):
        async def execute(
            self,
            secret: str,
            ttl_seconds: int | None,
            passphrase: str | None,
    ) -> CreateSecretDto: ...



class CreateSecretController:
    def __init__(self, create_usecase: CreateSecretUsecaseProtocol) -> None:
        self.create_usecase = create_usecase


    async def create_secret(
            self,
            create_request_data: requests.SecretPostRequest,
        ) -> responses.SecretPostResponse:
        try:
            response_data = await self.create_usecase.execute(
                secret=create_request_data.secret,
                ttl_seconds=create_request_data.ttl_seconds,
                passphrase=create_request_data.passphrase,
            )
            return responses.SecretPostResponse(secret_key=response_data.secret_id)
        except AppError as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            ) from e
