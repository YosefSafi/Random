from dataclasses import dataclass
from typing import List, Dict, Any
from ...core.ports.repository import ITaskRepository

@dataclass
class GetTasksQuery:
    limit: int = 100
    offset: int = 0

class GetTasksHandler:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    async def handle(self, query: GetTasksQuery) -> List[Dict[str, Any]]:
        tasks = await self.repository.get_all(limit=query.limit, offset=query.offset)
        return [
            {
                "id": str(task.id.value),
                "title": task._title,
                "project_id": str(task._project_id.value),
                "status": task._status,
                "version": task._version
            }
            for task in tasks
        ]
