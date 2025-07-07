from app.db.models import Allocation
from app.services.allocation_service import AllocationService
from tests.conftest import InMemoryDatabase


def test_allocate_first_id(test_db: InMemoryDatabase, allocation_service: AllocationService) -> None:
    test_db.clear()
    allocated_id = allocation_service.allocate()
    assert allocated_id == 1


def test_allocate_multiple_ids(test_db: InMemoryDatabase, allocation_service: AllocationService) -> None:
    test_db.clear()
    ids = [allocation_service.allocate() for _ in range(5)]
    assert ids == [1, 2, 3, 4, 5]


def test_allocation_persists_in_db(test_db: InMemoryDatabase, allocation_service: AllocationService) -> None:
    test_db.clear()
    allocation_service.allocate()
    allocation_service.allocate()

    with allocation_service.database.get_db_session() as session:
        allocation = session.query(Allocation).first()
        assert allocation.last_allocated_id == 2
