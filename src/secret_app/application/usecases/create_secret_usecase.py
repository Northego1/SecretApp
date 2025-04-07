import uuid
from datetime import UTC, datetime
from typing import Protocol

from core.logger import get_logger
from secret_app.application.dto import CreateSecretDto
from secret_app.application.uow_protocol import UowProtocol
from secret_app.domain.secret import Secret
from secret_app.domain.secret_log import ActionType, SecretLog

log = get_logger(__name__)


class SecretRepositoryProtocol(Protocol):
        async def save_secret(self, secret: Secret) -> None: ...

class SecretLogRepositoryProtocol(Protocol):
        async def create(self, secret_log: SecretLog) -> None: ...

class RepositoryProtocol(Protocol):
    secret_repository: SecretRepositoryProtocol
    secret_log_repository: SecretLogRepositoryProtocol

class SecurityProtocol(Protocol):
    def encrypt(self, data: str | bytes) -> bytes: ...
    def encrypt_passphrase(self, passphrase: str) -> bytes: ...

class CreateSecretUsecase:
    def __init__(
            self,
            uow: UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(
            self,
            secret: str,
            ttl_seconds: int | None,
            passphrase: str | None,
    ) -> CreateSecretDto:
        log.info("Executing CreateSecretUsecase")
        new_secret_id = uuid.uuid4()
        now = datetime.now(UTC)
        log.debug("Creating new secret with id: '%s'", new_secret_id)

        secret_domain = Secret(
            id=new_secret_id,
            secret=self.security.encrypt(secret),
            ttl_seconds=ttl_seconds,
            is_readed=False,
            passphrase=self.security.encrypt_passphrase(passphrase) if passphrase else None,
            created_at=now,
        )
        log.debug("Creating SecretLog for secret with id: '%s'", new_secret_id)
        secret_log = SecretLog(
            id=uuid.uuid4(),
            secret_id=secret_domain.id,
            action_type=ActionType.CREATE,
            created_at=now,
        )
        async with self.uow.transaction() as repo:
            await repo.secret_repository.save_secret(secret_domain)
            await repo.secret_log_repository.create(secret_log)
            log.info("CreateSecretUseCase executed successfully for secret_id: '%s'", new_secret_id)
            return CreateSecretDto(
                secret_id=new_secret_id,
            )
