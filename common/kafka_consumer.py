from aiokafka import AIOKafkaConsumer
from typing import Callable


class KafkaConsumerSessionManager:
    def __init__(self, kafka_conf):
        self._kafka_conf = kafka_conf
        self._topics = None
        self._kafka_consumer: AIOKafkaConsumer = None
        self._wrapper_function = None

    async def init_consumer(self, topics, wrapper_function: Callable[[bytes], None]):
        self._topics = topics
        self._kafka_consumer = AIOKafkaConsumer(self._topics, **self._kafka_conf)
        self._wrapper_function = wrapper_function

    async def stop(self):
        return await self._kafka_consumer.stop()

    async def consume(self):
        if self._topics is None or self._wrapper_function is None:
            raise Exception("Kafka consumer is not initialized")

        consumer = self._kafka_consumer
        await consumer.start()
        try:
            async for msg in consumer:
                await self._wrapper_function(msg)
        finally:
            await consumer.stop()
