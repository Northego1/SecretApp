from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class CreateSecretDto:
    secret_id: UUID


@dataclass(slots=True)
class ReadSecretDto(CreateSecretDto):
    secret: str
