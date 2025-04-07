import uuid
from datetime import UTC, datetime
from typing import Protocol

from core.logger import get_logger
from secret_app.application.exceptions import (
        SecretNotFoundError,
        SecretPassphraseError,
)
from secret_app.application.uow_protocol import UowProtocol
from secret_app.domain.secret import Secret
from secret_app.domain.secret_log import ActionType, SecretLog

log = get_logger(__name__)


class SecretRepositoryProtocol(Protocol):
    async def get_secret(self, secret_id: uuid.UUID) -> Secret | None: ...
    async def delete_secret(self, secret_id: uuid.UUID) -> None: ...

class SecretLogRepositoryProtocol(Protocol):
        async def create(self, secret_log: SecretLog) -> None: ...

class RepositoryProtocol(Protocol):
    secret_repository: SecretRepositoryProtocol
    secret_log_repository: SecretLogRepositoryProtocol

class SecurityProtocol(Protocol):
    def check_passphrase(self, passphrase: str, hashed_passphrase: bytes) -> bool: ...


class DeleteSecretUsecase:
    def __init__(
            self,
            uow: UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security

    async def execute(
            self,
            secret_id: uuid.UUID,
            passphrase: str | None,
    ) -> None:
        log.info("Executing DeleteSecretUseCase for secret_id: '%s'", secret_id)
        async with self.uow.transaction() as repo:
            if not (secret := await repo.secret_repository.get_secret(secret_id)):
                log.error("Secret with id: '%s' not found", secret_id)
                raise SecretNotFoundError(
                    status_code=404,
                    detail=f"Secret with id: {secret_id!r} not found",
                )
            if secret.passphrase:
                log.info("Checking passphrase for secret with id: '%s'", secret_id)
                if not passphrase:
                    log.error(
                        "Passphrase required for secret with id: '%s'", secret_id,
                    )
                    raise SecretPassphraseError(
                        status_code=403,
                        detail=f"This action by secret with id: {secret_id!r} requires a passphrase",
                    )
                if not self.security.check_passphrase(
                    passphrase, secret.passphrase,
                ):
                    log.error(
                        "Invalid passphrase for secret with id: '%s'", secret_id,
                    )
                    raise SecretPassphraseError(
                        status_code=403,
                        detail=f"Invalid passphrase for secret with id: {secret_id!r}",
                    )
                secret_log = SecretLog(
                    id=uuid.uuid4(),
                    secret_id=secret.id,
                    action_type=ActionType.DELETE,
                    created_at=datetime.now(UTC),
                )
                log.info("Deleting secret with id: '%s'", secret_id)
                await repo.secret_log_repository.create(secret_log)
                await repo.secret_repository.delete_secret(secret_id)



