from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ISearchService(ABC):
    @abstractmethod
    async def index_task(self, task_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        pass
