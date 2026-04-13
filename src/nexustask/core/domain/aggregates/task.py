from typing import List, Optional
from datetime import datetime
from ..events import TaskCreatedEvent, TaskStatusChangedEvent, DomainEvent
from ..value_objects import TaskId, ProjectId

class TaskAggregate:
    """
    Event-sourced aggregate root for Tasks.
    """
    def __init__(self, id: TaskId, title: str, project_id: ProjectId):
        self._id = id
        self._title = title
        self._project_id = project_id
        self._status = "TODO"
        self._uncommitted_events: List[DomainEvent] = []
        self._version = 0

    @property
    def id(self) -> TaskId:
        return self._id

    @property
    def events(self) -> List[DomainEvent]:
        return self._uncommitted_events

    def clear_events(self):
        self._uncommitted_events.clear()

    @classmethod
    def create(cls, id: TaskId, title: str, project_id: ProjectId) -> 'TaskAggregate':
        task = cls(id, title, project_id)
        task._apply(TaskCreatedEvent(
            occurred_on=datetime.utcnow(),
            task_id=str(id.value),
            title=title,
            project_id=str(project_id.value)
        ))
        return task

    def change_status(self, new_status: str, reason: Optional[str] = None):
        if self._status == new_status:
            return
        old_status = self._status
        self._status = new_status
        self._apply(TaskStatusChangedEvent(
            occurred_on=datetime.utcnow(),
            task_id=str(self.id.value),
            old_status=old_status,
            new_status=new_status,
            reason=reason
        ))

    def _apply(self, event: DomainEvent):
        self._uncommitted_events.append(event)
        self._version += 1
