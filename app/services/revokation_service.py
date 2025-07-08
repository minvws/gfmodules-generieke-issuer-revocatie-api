from datetime import datetime, timezone

from app.db.db import Database
from app.db.models import Allocation, Revocation


class RevocationService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def unrevoke(self, index: int) -> None:
        with self.database.get_db_session() as session:
            revocation = session.query(Revocation).filter_by(index=index).first()
            if not revocation:
                raise ValueError(f"Index {index} is not revoked")

            # Remove the revocation entry
            session.delete(revocation)
            session.commit()

    def revoke(self, index: int, reason: str | None = None) -> Revocation:
        with self.database.get_db_session() as session:
            # Check if the index is already revoked
            existing_revocation = session.query(Revocation).filter_by(index=index).first()
            if existing_revocation:
                raise ValueError(f"Index {index} is already revoked")

            # Check if the index is more than 0
            if index < 0:
                raise ValueError("Index must be a non-negative integer")

            # Check if the index is less than the last allocated ID
            allocation = session.query(Allocation).first()
            if allocation is None or index > allocation.last_allocated_id:
                raise ValueError("Index is out of bounds of the allocated IDs")

            # Create a new revocation entry
            revocation = Revocation(
                index=index,
                reason=reason,
                revoked_at=datetime.now(timezone.utc),
            )
            session.add(revocation)
            session.commit()
            session.refresh(revocation)
            return revocation

    def get_revoked_indices(self) -> list[int]:
        with self.database.get_db_session() as session:
            revocations = session.query(Revocation).all()
            return [rev.index for rev in revocations]
