from typing import Sequence

from sqlalchemy import select

from app.db.decorator import repository
from app.db.models import Revocation
from app.db.repositories import RepositoryBase


@repository(Revocation)
class RevocationRepository(RepositoryBase):
    def find_all(self) -> Sequence[Revocation]:
        stmt = select(Revocation)
        return self.db_session.session.execute(stmt).scalars().all()  # type: ignore[no-any-return]
