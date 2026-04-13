from ...core.ports.repository import ITaskRepository
from ...core.domain.aggregates.task import TaskAggregate
from ...core.domain.value_objects import TaskId
from typing import Optional, List

class PostgresTaskRepository(ITaskRepository):
    """
    Async SQLAlchemy implementation of the Task Repository.
    """
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_id(self, task_id: TaskId) -> Optional[TaskAggregate]:
        # Complex SQLAlchemy async query here
        pass

    async def save(self, task: TaskAggregate) -> None:
        # Save to Postgres, and append to EventStore in the same transaction
        pass

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[TaskAggregate]:
        return []
