import uuid
from typing import Protocol

from fastapi import HTTPException, Response

from core.exceptions import AppError
from core.logger import get_logger
from secret_app.application.dto import ReadSecretDto
from secret_app.presentation.schemas import responses

log = get_logger(__name__)


class GetSecretUsecaseProtocol(Protocol):
    async def execute(self, secret_id: uuid.UUID) -> ReadSecretDto: ...


class GetSecretController:
    def __init__(
        self,
        get_secret_uc: GetSecretUsecaseProtocol,
    ) -> None:
        self.get_secret_uc = get_secret_uc

    async def get_secret(
        self, secret_id: uuid.UUID, response: Response,
    ) -> responses.SecretGetReponse:
        try:
            log.debug("Calling get secret usecase")
            uc_response = await self.get_secret_uc.execute(
                secret_id=secret_id,
            )
            response.headers["Cache-Control"] = "no-store"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return responses.SecretGetReponse(
                secret=uc_response.secret,
            )
        except AppError as e:
            log.debug("Returing error response with status code: %s", e.status_code)
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            ) from e
