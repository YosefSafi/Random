from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    REDIS_URL: str = "redis://localhost:6379"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    JIRA_URL: Optional[str] = None
    JIRA_API_KEY: Optional[str] = None
    TESTING: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
