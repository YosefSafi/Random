from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..application.commands.create_task import CreateTaskHandler
from .database.repository import PostgresTaskRepository
from .message_bus.kafka_bus import KafkaEventBus

class DummyProducer:
    async def send_and_wait(self, topic: str, payload: bytes):
        pass

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

def get_create_task_handler() -> CreateTaskHandler:
    repository = PostgresTaskRepository(AsyncSessionLocal)
    event_bus = KafkaEventBus(DummyProducer())
    return CreateTaskHandler(repository, event_bus)

async def init_db():
    from .database.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
