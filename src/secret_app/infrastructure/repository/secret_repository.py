from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from secret_app.domain.secret import Secret


class SecretRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_secret(self, secret_id: UUID) -> Secret | None:
        ...

    async def save_secret(self, secret: Secret) -> UUID:
        ...

    async def delete_secret(self, secret_id: UUID) -> None:
        ...