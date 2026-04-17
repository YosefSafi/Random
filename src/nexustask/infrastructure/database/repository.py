from sqlalchemy import select
from typing import Optional, List
import uuid
import json

from ...core.ports.repository import ITaskRepository
from ...core.domain.aggregates.task import TaskAggregate
from ...core.domain.value_objects import TaskId, ProjectId
from .models import TaskModel, EventStoreModel

class PostgresTaskRepository(ITaskRepository):
    """
    Async SQLAlchemy implementation of the Task Repository.
    """
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_id(self, task_id: TaskId) -> Optional[TaskAggregate]:
        async with self.session_factory() as session:
            result = await session.execute(select(TaskModel).where(TaskModel.id == str(task_id.value)))
            task_model = result.scalar_one_or_none()
            if not task_model:
                return None
            
            project_id = ProjectId(uuid.UUID(task_model.project_id))
            task = TaskAggregate(task_id, task_model.title, project_id)
            task._status = task_model.status
            task._version = task_model.version
            return task

    async def save(self, task: TaskAggregate) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                task_model = await session.get(TaskModel, str(task.id.value))
                if not task_model:
                    task_model = TaskModel(
                        id=str(task.id.value),
                        title=task._title,
                        project_id=str(task._project_id.value),
                        status=task._status,
                        version=task._version
                    )
                    session.add(task_model)
                else:
                    task_model.title = task._title
                    task_model.status = task._status
                    task_model.version = task._version

                for event in task.events:
                    event_model = EventStoreModel(
                        aggregate_id=str(task.id.value),
                        event_type=event.__class__.__name__,
                        payload=json.dumps(event.__dict__, default=str),
                        occurred_on=event.occurred_on
                    )
                    session.add(event_model)

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[TaskAggregate]:
        async with self.session_factory() as session:
            result = await session.execute(select(TaskModel).limit(limit).offset(offset))
            task_models = result.scalars().all()
            
            tasks = []
            for task_model in task_models:
                task_id = TaskId(uuid.UUID(task_model.id))
                project_id = ProjectId(uuid.UUID(task_model.project_id))
                task = TaskAggregate(task_id, task_model.title, project_id)
                task._status = task_model.status
                task._version = task_model.version
                tasks.append(task)
            
            return tasks
