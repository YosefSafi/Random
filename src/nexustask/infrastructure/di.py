from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..application.commands.create_task import CreateTaskHandler
from ..application.queries.get_tasks import GetTasksHandler
from .database.repository import PostgresTaskRepository, GenericPostgresRepository
from .message_bus.kafka_bus import KafkaEventBus
from .message_bus.kafka_producer import RealKafkaProducer
from ..config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

def get_task_repository() -> PostgresTaskRepository:
    return PostgresTaskRepository(AsyncSessionLocal)

def get_generic_repository() -> GenericPostgresRepository:
    return GenericPostgresRepository(AsyncSessionLocal)

class DummyCache:
    async def get(self, key): return None
    async def set(self, key, value, expire=None): pass

class SimpleEventBus:
    async def publish(self, event_type, payload): pass

class MockEventBus:
    async def publish(self, event): pass

def get_create_task_handler() -> CreateTaskHandler:
    repository = get_task_repository()
    if settings.TESTING:
        event_bus = MockEventBus()
    else:
        event_bus = KafkaEventBus(RealKafkaProducer(settings.KAFKA_BOOTSTRAP_SERVERS))
    return CreateTaskHandler(repository, event_bus, get_search_service())

def get_tasks_handler() -> GetTasksHandler:
    repository = get_task_repository()
    return GetTasksHandler(repository)

def get_enterprise_service(service_cls):
    return service_cls(get_generic_repository(), SimpleEventBus(), DummyCache())

from .search.elasticsearch_service import ElasticsearchService
from ..core.ports.search import ISearchService

class MockSearchService:
    async def index_task(self, task_data): pass
    async def search_tasks(self, query): return []

def get_search_service() -> ISearchService:
    if settings.TESTING:
        return MockSearchService()
    return ElasticsearchService(settings.ELASTICSEARCH_URL)

async def init_db():
    from .database.models import Base
    from .database.massive_models import Base as MassiveBase
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(MassiveBase.metadata.create_all)
