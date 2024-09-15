from fastapi import FastAPI, Response, Request
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from controllers.agreement import agreement_router
from controllers.product import product_router
from controllers.schedule import schedule_router
from controllers.client import client_router
from jobs.start import check_dates, send_to_orig
from kafka.producer import producer
from kafka.consumer import consumer, create_schedule, consumer_payment, payment_schedule
from common.config import settings
import asyncio

description = """
## Product

* **GET /product** Возвращает массив продуктов, или пустой массив, если продуктов нет.
* **GET /product/{product_code}** Возвращает информацию по продукту по коду {product_code}. Если такого продукта не существует - 404 Not Found
* **POST /product** Принимает JSON. Создает новый продукт, записывает его в базу. Новый продукт может быть сразу получен методами GET
* **DELETE /product/{product_code}** Удаляет продукт с кодом {product_code}. Возвращает код 204 без тела

## Client

* **GET /client** Возвращает массив клиентов, или пустой массив, если продуктов нет.
* **GET /product/{client_id}** Возвращает информацию по клиенту по id. Если такого клиента не существует - 404 Not Found

## Agreement

* **GET /agreement** Возвращает все договора
* **GET /agreement/{id}** Возвращает договор по id
* **GET /agreement/status/new** Возвращает все договора со статусом NEW
* **GET /agreement/client/{id}** Возвращает все договора по client_id
* **POST /{agreement_id}/update** Обновляет статус у договора с agreement_id
* **POST /agreement** Принимает JSON. Создание заявки на кредит. Если все успешно и нет ошибок - записывает информацию в таблицу agreement. Возвращает код с определенным телом

## Schedule

* **POST /schedule** Принимает agreement_id. Создаёт график платежей для договора с agreement_id
* **GET /schedule/{id}** Возвращает график по id договора
"""

tags_metadata = [
    {
        "name": "product",
        "description": "Операции с продуктами",
    },
    {
        "name": "agreement",
        "description": "Операции с заявками на кредит",
    },
    {
        "name": "schedule",
        "description": "Операции с графиками по договорам",
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_dates, "interval", seconds=settings.job_check_dates_seconds)
    scheduler.add_job(send_to_orig, "interval", seconds=settings.job_send_to_orig_seconds)
    scheduler.start()
    await producer.init_producer()
    await consumer.init_consumer(settings.kafka_scoring_response_topic, create_schedule)
    await consumer_payment.init_consumer(settings.kafka_schedule_payment_topic, payment_schedule)
    task1 = asyncio.create_task(consumer.consume())
    task2 = asyncio.create_task(consumer_payment.consume())
    yield
    await producer.stop()
    await consumer.stop()
    await consumer_payment.stop()

app = FastAPI(description=description, openapi_tags=tags_metadata, lifespan=lifespan)
app.include_router(agreement_router)
app.include_router(product_router)
app.include_router(schedule_router)
app.include_router(client_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == '/agreement':
        return JSONResponse(content={"message": "Типы данных не соответствуют формату"}, status_code=400)
    return Response(status_code=400)
