import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.models import Base
from app.services.allocation_service import AllocationService
from app.services.revokation_service import RevocationService


class InMemoryDatabase:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_db_session(self) -> Session:
        return self.SessionLocal()

    def clear(self) -> None:
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


TEST_DB = InMemoryDatabase()


@pytest.fixture
def test_db() -> InMemoryDatabase:
    return TEST_DB


@pytest.fixture
def allocation_service() -> AllocationService:
    return AllocationService(database=TEST_DB)  # type: ignore


@pytest.fixture
def revocation_service() -> RevocationService:
    return RevocationService(database=TEST_DB)  # type: ignore
