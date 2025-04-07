from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class ActionType(Enum):
    CREATE = "create"
    READ = "read"
    DELETE = "delete"


@dataclass(slots=True)
class SecretLog:
    id: UUID
    secret_id: UUID
    action_type: ActionType
    created_at: datetime
