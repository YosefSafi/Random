from dataclasses import dataclass
from ...core.ports.repository import ITaskRepository
from ...core.ports.event_bus import IEventBus
from ...core.domain.aggregates.task import TaskAggregate
from ...core.domain.value_objects import TaskId, ProjectId
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class CreateTaskCommand:
    title: str
    project_id: str

class CreateTaskHandler:
    def __init__(self, repository: ITaskRepository, event_bus: IEventBus):
        self.repository = repository
        self.event_bus = event_bus

    async def handle(self, command: CreateTaskCommand) -> str:
        logger.info("handling_create_task", title=command.title)

        task_id = TaskId.generate()
        import uuid
        project_id = ProjectId(uuid.UUID(command.project_id))

        task = TaskAggregate.create(task_id, command.title, project_id)

        await self.repository.save(task)

        for event in task.events:
            await self.event_bus.publish(event)
        task.clear_events()

        logger.info("task_created", task_id=str(task_id.value))
        return str(task_id.value)
