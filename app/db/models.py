from __future__ import annotations

import datetime
import uuid

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Revocation(Base):
    __tablename__ = "revocations"

    id: Mapped[uuid.UUID] = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index: Mapped[int] = mapped_column("bit_index", Integer, nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column("reason", Text, nullable=True)
    revoked_at: Mapped[datetime.datetime] = mapped_column(
        "revoked", DateTime(timezone=True), nullable=False, default=datetime.datetime.now
    )

    def __repr__(self) -> str:
        return f"<Revocation(id={self.id}, index={self.index}, reason={self.reason}, revoked_at={self.revoked_at})>"


class Allocation(Base):
    __tablename__ = "allocations"

    id: Mapped[uuid.UUID] = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_allocated_id: Mapped[int] = mapped_column("last_allocated_id", Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Allocation(id={self.id}, last_allocated_id={self.last_allocated_id})>"
