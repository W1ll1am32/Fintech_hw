from fastapi import FastAPI
from contextlib import asynccontextmanager
from kafka.consumer import consumer, scoring
from kafka.producer import producer
from common.config import settings
import asyncio


tags_metadata = [
    {
        "name": "scoring",
        "description": "Проверка договоров и вердикт заявкам",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await producer.init_producer()
    await consumer.init_consumer(settings.kafka_scoring_topic, scoring)
    task = asyncio.create_task(consumer.consume())
    yield
    await producer.stop()
    await consumer.stop()


app = FastAPI(openapi_tags=tags_metadata, lifespan=lifespan)

"""
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
"""