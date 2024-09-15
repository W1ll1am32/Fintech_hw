from common.kafka_producer import KafkaProducerSessionManager
from common.config import settings
from aiokafka import AIOKafkaProducer

producer = KafkaProducerSessionManager({"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}"})


async def get_producer() -> AIOKafkaProducer:
    async with producer.session() as session:
        yield session
