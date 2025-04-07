import uuid
from datetime import UTC, datetime
from typing import Protocol

from core.logger import get_logger
from secret_app.application.dto import ReadSecretDto
from secret_app.application.exceptions import (
    SecretAlreadyReadError,
    SecretExpiredError,
    SecretNotFoundError,
)
from secret_app.application.uow_protocol import UowProtocol
from secret_app.domain.secret import Secret
from secret_app.domain.secret_log import ActionType, SecretLog

log = get_logger(__name__)


class SecretRepositoryProtocol(Protocol):
    async def get_secret(self, secret_id: uuid.UUID) -> Secret | None: ...
    async def update_secret(self, secret: Secret) -> None: ...


class SecretLogRepositoryProtocol(Protocol):
    async def create(self, secret_log: SecretLog) -> None: ...


class RepositoryProtocol(Protocol):
    secret_repository: SecretRepositoryProtocol
    secret_log_repository: SecretLogRepositoryProtocol


class SecurityProtocol(Protocol):
    def decrypt(self, encrypted_data: bytes | str) -> str: ...


class GetSecretUsecase:
    def __init__(
        self,
        uow: UowProtocol[RepositoryProtocol],
        security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security

    async def execute(self, secret_id: uuid.UUID) -> ReadSecretDto:
        log.debug("Executing ReadSecretUseCase for secret_id: '%s'", secret_id)
        async with self.uow.transaction() as repo:
            if not (secret := await repo.secret_repository.get_secret(secret_id)):
                log.error("Secret with id: '%s' not found", secret_id)
                raise SecretNotFoundError(
                    status_code=404,
                    detail=f"Secret with id: {secret_id!r} not found",
                )
            if secret.is_readed:
                log.warning("Secret with id: '%s' has already been read", secret_id)
                raise SecretAlreadyReadError(
                    status_code=400,
                    detail=f"Secret with id: {secret_id!r} has already been read",
                )
            if secret.is_expired():
                log.warning("Secret with id: '%s' has expired", secret_id)
                raise SecretExpiredError(
                    status_code=410,
                    detail=f"Secret with id: {secret_id!r} has expired",
                )
            log.info("Secret with id: '%s' retrieved successfully", secret_id)

            secret_log = SecretLog(
                id=uuid.uuid4(),
                secret_id=secret.id,
                action_type=ActionType.READ,
                created_at=datetime.now(UTC),
            )
            await repo.secret_log_repository.create(secret_log)
            log.info("SecretLog created for secret_id: '%s'", secret_id)

            secret.is_readed = True
            await repo.secret_repository.update_secret(secret)
            log.info("Secret with id: '%s' marked as read", secret_id)

            decrypted_secret = self.security.decrypt(secret.secret)
            log.debug("Secret with id: '%s' decrypted successfully", secret_id)

            log.info("ReadSecretUseCase executed successfully for secret_id: '%s'", secret_id)
            return ReadSecretDto(
                secret_id=secret.id,
                secret=decrypted_secret,
            )
