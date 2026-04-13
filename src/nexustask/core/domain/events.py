from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class DomainEvent:
    occurred_on: datetime

@dataclass(frozen=True)
class TaskCreatedEvent(DomainEvent):
    task_id: str
    title: str
    project_id: str

@dataclass(frozen=True)
class TaskStatusChangedEvent(DomainEvent):
    task_id: str
    old_status: str
    new_status: str
    reason: Optional[str] = None
