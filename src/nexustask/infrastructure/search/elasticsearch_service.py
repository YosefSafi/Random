from elasticsearch import AsyncElasticsearch
from ...core.ports.search import ISearchService
from typing import Any, Dict, List
import structlog

logger = structlog.get_logger(__name__)

class ElasticsearchService(ISearchService):
    def __init__(self, es_url: str):
        self.client = AsyncElasticsearch(es_url)
        self.index_name = "tasks"

    async def index_task(self, task_data: Dict[str, Any]) -> None:
        try:
            await self.client.index(
                index=self.index_name,
                id=task_data["id"],
                document=task_data
            )
            logger.info("task_indexed", task_id=task_data["id"])
        except Exception as e:
            logger.error("indexing_failed", error=str(e))
            raise

    async def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        try:
            response = await self.client.search(
                index=self.index_name,
                query={
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description", "status"]
                    }
                }
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            logger.error("search_failed", error=str(e))
            return []

    async def close(self):
        await self.client.close()
