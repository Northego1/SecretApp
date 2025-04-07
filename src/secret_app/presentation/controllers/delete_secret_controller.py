import uuid
from typing import Protocol

from fastapi import HTTPException

from core.exceptions import AppError
from core.logger import get_logger
from secret_app.presentation.schemas import requests

log = get_logger(__name__)


class DeleteSecretUsecaseProtocol(Protocol):
    async def execute(
        self,
        secret_id: uuid.UUID,
        passphrase: str | None,
    ) -> None: ...


class DeleteSecretController:
    def __init__(
        self,
        delete_secret_uc: DeleteSecretUsecaseProtocol,
    ) -> None:
        self.delete_secret_uc = delete_secret_uc

    async def delete_secret(
        self,
        secret_id: uuid.UUID,
        requested_data: requests.SecretDeleteRequest,
    ) -> None:
        try:
            log.debug("Calling delete secret usecase")
            return await self.delete_secret_uc.execute(
                secret_id=secret_id,
                passphrase=requested_data.passphrase,
            )
        except AppError as e:
            log.debug("Returing error response with status code: %s", e.status_code)
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            ) from e
