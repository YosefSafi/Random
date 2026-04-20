from celery import Celery
from ..config import settings
import asyncio
from ..plugins.jira_sync.plugin import JiraSyncPlugin
import structlog

logger = structlog.get_logger(__name__)

celery_app = Celery(
    "nexustask",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="nexustask.sync_with_jira")
def sync_with_jira_task(task_id: str):
    """
    Background task to sync a task with Jira.
    """
    if not settings.JIRA_URL or not settings.JIRA_API_KEY:
        logger.warning("jira_sync_skipped", reason="missing_config")
        return False

    plugin = JiraSyncPlugin(settings.JIRA_API_KEY, settings.JIRA_URL)
    
    # Run async function in sync context
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(plugin.sync_task(task_id))
    
    return success
