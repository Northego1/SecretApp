import uuid
from datetime import UTC, datetime

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import (
    UUID,
    Boolean,
    DateTime,
    Integer,
    LargeBinary,
)

from core.database import Base
from secret_app.domain.secret_log import ActionType


class SecretModel(Base):
    __tablename__ = "secrets"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    secret: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_readed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    passphrase: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    ttl_seconds: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(UTC),
    )

    secret_logs: Mapped["SecretLogModel"] = relationship(
        "secret_app.infrastructure.models.SecretLogModel", back_populates="secret",
    )


class SecretLogModel(Base):
    __tablename__ = "secret_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    action_type: Mapped[ActionType] = mapped_column(
        SQLAlchemyEnum(ActionType, native_enum=False), nullable=False,
    )
    secret_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("secrets.id", ondelete="SET NULL"), nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(UTC),
    )

    secret: Mapped["SecretModel"] = relationship(
        "secret_app.infrastructure.models.SecretModel", back_populates="secret_logs",
    )
