from fastapi import FastAPI
from controllers.product import product_router
from controllers.agreement import agreement_router
from controllers.application import application_router
from controllers.schedule import schedule_router

description = """
## Product

* **GET /product** Возвращает массив продуктов, или пустой массив, если продуктов нет.
* **GET /product/{product_code}** Возвращает информацию по продукту по коду {product_code}. Если такого продукта не существует - 404 Not Found
* **POST /product** Принимает JSON. Создает новый продукт, записывает его в базу. Новый продукт может быть сразу получен методами GET

## Agreement

* **POST /agreement** Принимает JSON. Создание договора. Если все успешно и нет ошибок - записывает информацию в таблицу agreement. Возвращает код с определенным телом
* **GET /agreement/{client_id}** Принимает id клиента. Возвращает все договоры клиента с таким id

## Application

* **POST /application/{application_id}/close** Принимает запрос на удаление заявки. Если все успешно - возвращает HTTPResponse и заявка удаляется иначе HTTPException

## Schedule

* **GET /schedule/{agreement_id}** Принимает id договора. Возвращает график платежей по данному договору

"""

tags_metadata = [
    {
        "name": "product",
        "description": "Операции с продуктами",
    },
    {
        "name": "agreement",
        "description": "Операции с договорами",
    },
    {
        "name": "application",
        "description": "Операции с заявками на кредит",
    },
    {
        "name": "schedule",
        "description": "Операции с графиками платежей",
    }
]

app = FastAPI(description=description, openapi_tags=tags_metadata)
app.include_router(product_router)
app.include_router(agreement_router)
app.include_router(application_router)
app.include_router(schedule_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
@app.get("/hello/{name}")
async def say_hello(name: str):
    with async_timeout.timeout(59):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url="http://127.0.0.1:8000/hello/{}".format(str))
            data = await response.json()
            return {"message": f"Hello {data['message']}"}
"""

