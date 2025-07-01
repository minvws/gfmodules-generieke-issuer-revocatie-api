import pytest

from app.db.models import Allocation
from app.services.revokation_service import RevocationService
from tests.conftest import InMemoryDatabase


def create_allocation(test_db: InMemoryDatabase, last_allocated_id: int = 10) -> None:
    with test_db.get_db_session() as session:
        allocation = Allocation(last_allocated_id=last_allocated_id)
        session.add(allocation)
        session.commit()


def test_successful_revoke(revocation_service: RevocationService, test_db: InMemoryDatabase) -> None:
    test_db.clear()
    create_allocation(test_db, last_allocated_id=10)
    revocation = revocation_service.revoke(index=5, reason="Test revoke")
    assert revocation.index == 5
    assert revocation.reason == "Test revoke"
    assert revocation.revoked_at is not None


def test_revoke_twice_fails(revocation_service: RevocationService, test_db: InMemoryDatabase) -> None:
    test_db.clear()
    create_allocation(test_db, last_allocated_id=10)
    revocation_service.revoke(index=3)
    with pytest.raises(ValueError, match="already revoked"):
        revocation_service.revoke(index=3)


def test_revoke_negative_index_fails(revocation_service: RevocationService, test_db: InMemoryDatabase) -> None:
    test_db.clear()
    create_allocation(test_db, last_allocated_id=10)
    with pytest.raises(ValueError, match="non-negative integer"):
        revocation_service.revoke(index=-1)


def test_revoke_out_of_bounds_fails(revocation_service: RevocationService, test_db: InMemoryDatabase) -> None:
    test_db.clear()
    create_allocation(test_db, last_allocated_id=5)
    with pytest.raises(ValueError, match="out of bounds"):
        revocation_service.revoke(index=6)


def test_revoke_without_allocation_fails(test_db: InMemoryDatabase, revocation_service: RevocationService) -> None:
    test_db.clear()
    with pytest.raises(ValueError, match="out of bounds"):
        revocation_service.revoke(index=0)
