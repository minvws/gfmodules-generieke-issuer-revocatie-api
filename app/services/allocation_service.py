from app.db.db import Database
from app.db.models import Allocation


class AllocationService:
    def __init__(self, database: Database):
        self.database = database

    def allocate(self) -> int:
        """
        Allocate a new ID. It is guaranteed to be unique and not previously allocated.
        """
        with self.database.get_db_session() as session:
            allocation = session.query(Allocation).with_for_update().first()
            if allocation is None:
                allocation = Allocation(last_allocated_id=1)
                session.add(allocation)
            else:
                allocation.last_allocated_id += 1

            session.commit()
            return allocation.last_allocated_id  # type: ignore
