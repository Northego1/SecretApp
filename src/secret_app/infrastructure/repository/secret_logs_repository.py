from sqlalchemy.ext.asyncio import AsyncSession

from secret_app.domain.secret_log import SecretLog


class SecretLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, secret_log: SecretLog) -> None:
        ...
