import contextlib
import json

from aiokafka import AIOKafkaProducer


class KafkaProducerSessionManager:
    def __init__(self, kafka_conf):
        self._kafka_conf = kafka_conf
        self._kafka_producer: AIOKafkaProducer = None

    async def init_producer(self):
        self._kafka_producer = AIOKafkaProducer(**self._kafka_conf)
        await self._kafka_producer.start()

    async def stop(self):
        await self._kafka_producer.stop()

    @contextlib.asynccontextmanager
    async def session(self):
        if self._kafka_producer is None:
            raise Exception("Kafka producer is not initialized")
        yield self._kafka_producer


async def send_message(producer: AIOKafkaProducer, topic: str, value=None, key=None):
    return await producer.send(topic, json.dumps(value).encode("ascii"), key=key)
