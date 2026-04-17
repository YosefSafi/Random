from ...core.ports.event_bus import IEventBus
from ...core.domain.events import DomainEvent
import json

class KafkaEventBus(IEventBus):
    def __init__(self, producer):
        self.producer = producer

    async def publish(self, event: DomainEvent) -> None:
        # Serialize and publish to Kafka topics
        topic = f"nexustask.events.{event.__class__.__name__}"
        payload = json.dumps({"event": str(event)}).encode('utf-8')
        await self.producer.send_and_wait(topic, payload)
