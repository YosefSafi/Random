from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class TaskId:
    value: uuid.UUID

    @classmethod
    def generate(cls) -> 'TaskId':
        return cls(uuid.uuid4())

@dataclass(frozen=True)
class ProjectId:
    value: uuid.UUID
