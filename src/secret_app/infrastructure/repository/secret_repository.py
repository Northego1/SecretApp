from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import get_logger
from secret_app.domain.secret import Secret
from secret_app.infrastructure.models import SecretModel

log = get_logger(__name__)


class SecretRepository:
    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ) -> None:
        self.session = session
        self.redis = redis


    async def get_secret(self, secret_id: UUID) -> Secret | None:
        query = select(SecretModel).where(SecretModel.id == secret_id).with_for_update()
        log.debug("Executing query to get secret with id: '%s'", secret_id)
        result = await self.session.execute(query)
        result.scalars()
        if secret := result.scalars().first():
            return Secret(
                id=secret.id,
                secret=secret.secret,
                is_read=secret.is_read,
                passphrase=secret.passphrase,
                ttl_seconds=secret.ttl_seconds,
                created_at=secret.created_at,
            )
        return None


    async def create_secret(self, secret: Secret) -> None:
        secret_model = SecretModel(
            id=secret.id,
            secret=secret.secret,
            is_read=secret.is_read,
            passphrase=secret.passphrase,
            ttl_seconds=secret.ttl_seconds,
            created_at=secret.created_at,
        )
        log.debug("Adding secret to session: %s", secret_model.id)
        self.session.add(secret_model)


    async def delete_secret(self, secret_id: UUID) -> None:
        query = delete(SecretModel).where(SecretModel.id == secret_id)
        log.debug("Executing query to delete secret with id: '%s'", secret_id)
        await self.session.execute(query)


    async def update_secret(self, secret: Secret) -> None:
        query = (
            update(SecretModel)
            .where(SecretModel.id == secret.id)
            .values(
                is_read=secret.is_read,
            )
        )
        await self.session.execute(query)
