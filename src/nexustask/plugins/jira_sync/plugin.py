import logging
import httpx

logger = logging.getLogger(__name__)

class JiraSyncPlugin:
    """
    Bi-directional sync with Atlassian Jira Data Center.
    Added in v7.2.0 (2021) for Enterprise customers.
    """
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url
        logger.info("JiraSyncPlugin initialized.")

    async def sync_task(self, task_id: str):
        logger.info(f"Syncing task {task_id} with Jira at {self.url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.url}/rest/api/2/issue",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "fields": {
                            "project": {"key": "NEXUS"},
                            "summary": f"Syncing task {task_id}",
                            "description": "Task synced from NexusTask Enterprise",
                            "issuetype": {"name": "Task"}
                        }
                    }
                )
                response.raise_for_status()
                logger.info(f"Successfully synced task {task_id} to Jira.")
                return True
            except Exception as e:
                logger.error(f"Failed to sync task {task_id} to Jira: {e}")
                return False
