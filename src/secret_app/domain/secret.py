from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID


@dataclass(slots=True)
class Secret:
    id: UUID
    secret: bytes
    ttl_seconds: int | None
    is_readed: bool
    passphrase: bytes | None
    created_at: datetime


    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return (datetime.now(UTC) - self.created_at).total_seconds() > self.ttl_seconds



