from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.aggregates.task import TaskAggregate
from ..domain.value_objects import TaskId

class ITaskRepository(ABC):
    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Optional[TaskAggregate]:
        pass

    @abstractmethod
    async def save(self, task: TaskAggregate) -> None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[TaskAggregate]:
        pass
