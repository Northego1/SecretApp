from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from core.exceptions import AppError
from core.logger import get_logger

log = get_logger(__name__)

class SecretDomainError(AppError): ...


class SecretExpiredError(SecretDomainError): ...


class SecretAlreadyReadError(SecretDomainError): ...


@dataclass(slots=True)
class Secret:
    id: UUID
    secret: bytes
    ttl_seconds: int | None
    is_read: bool
    passphrase: bytes | None
    created_at: datetime


    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return (datetime.now(UTC) - self.created_at).total_seconds() > self.ttl_seconds


    def reveal(self) -> bytes:
        if self.is_read:
            log.warning("Secret with id: '%s' has already been read", self.id)
            raise SecretAlreadyReadError(
                status_code=400,
                detail=f"Secret with id: {self.id!r} has already been read",
            )
        if self.is_expired():
            log.warning("Secret with id: '%s' has expired", self.id)
            raise SecretExpiredError(
                status_code=410,
                detail=f"Secret with id: {self.id!r} has expired",
            )
        self.is_read = True
        return self.secret
