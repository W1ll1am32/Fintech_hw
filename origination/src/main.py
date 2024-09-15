import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.start import send_to_scoring
from controllers.application import application_router
from kafka.consumer import consumer_pe, consumer_scoring, create_application, change_status
from kafka.producer import producer
from common.config import settings


description = """
## application

* **GET /application/new** Возвращает все заявки со статусом NEW
* **GET /application** Возвращает все заявки
* **POST /{application_id}/update** Обновляет статус у заявки с application_id
* **POST /application/check** Принимает JSON. Проверяет является ли созданная заявка дубликатом. Если все успешно - передаёт данные в Scoring. Возвращает JSON со статусом
* **POST /application/{agreement_id}/close** Принимает запрос на удаление заявки. Передаёт её в PE. Если все успешно - возвращает HTTPResponse иначе HTTPException

"""


tags_metadata = [
    {
        "name": "application",
        "description": "Операции с заявками на кредит",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_to_scoring, "interval", seconds=settings.job_send_to_scoring_seconds)
    scheduler.start()
    await producer.init_producer()
    await consumer_pe.init_consumer(settings.kafka_agreement_topic, create_application)
    task1 = asyncio.create_task(consumer_pe.consume())
    await consumer_scoring.init_consumer(settings.kafka_scoring_response_topic, change_status)
    task2 = asyncio.create_task(consumer_scoring.consume())
    yield
    await producer.stop()
    await consumer_pe.stop()
    await consumer_scoring.stop()


app = FastAPI(description=description, openapi_tags=tags_metadata, lifespan=lifespan)
app.include_router(application_router)

"""
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
"""