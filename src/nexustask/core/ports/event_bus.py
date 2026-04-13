from abc import ABC, abstractmethod
from ..domain.events import DomainEvent

class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass
