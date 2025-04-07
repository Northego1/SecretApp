from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import get_logger
from secret_app.domain.secret_log import SecretLog
from secret_app.infrastructure.models import SecretLogModel

log = get_logger(__name__)


class SecretLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, secret_log: SecretLog) -> None:
        secret_log_model = SecretLogModel(
            id=secret_log.id,
            secret_id=secret_log.secret_id,
            action_type=secret_log.action_type,
            created_at=secret_log.created_at,
        )
        log.debug("Adding secret log to session: %s", secret_log_model.id)
        self.session.add(secret_log_model)
