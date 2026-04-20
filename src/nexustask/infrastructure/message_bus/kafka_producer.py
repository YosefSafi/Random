from kafka import KafkaProducer
import asyncio
import concurrent.futures
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)

class RealKafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[KafkaProducer] = None
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def _get_producer(self) -> KafkaProducer:
        if self._producer is None:
            logger.info("initializing_kafka_producer", bootstrap_servers=self.bootstrap_servers)
            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                retries=5
            )
        return self._producer

    async def send_and_wait(self, topic: str, payload: bytes):
        loop = asyncio.get_running_loop()
        producer = self._get_producer()
        
        def _send():
            future = producer.send(topic, payload)
            return future.get(timeout=10)

        try:
            await loop.run_in_executor(self._executor, _send)
            logger.debug("kafka_message_sent", topic=topic)
        except Exception as e:
            logger.error("kafka_send_failed", topic=topic, error=str(e))
            raise

    def close(self):
        if self._producer:
            self._producer.close()
            self._executor.shutdown()
