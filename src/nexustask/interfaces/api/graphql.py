import strawberry
from typing import List
from ...application.queries.get_tasks import GetTasksQuery, GetTasksHandler
from ...infrastructure.di import get_tasks_handler

@strawberry.type
class Task:
    id: str
    title: str
    project_id: str
    status: str
    version: int

@strawberry.type
class Query:
    @strawberry.field
    async def tasks(self, limit: int = 100, offset: int = 0) -> List[Task]:
        handler = get_tasks_handler()
        query = GetTasksQuery(limit=limit, offset=offset)
        tasks_data = await handler.handle(query)
        return [Task(**task) for task in tasks_data]

schema = strawberry.Schema(query=Query)
