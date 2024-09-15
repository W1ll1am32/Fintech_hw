from common.abstract_repository import AbstractRepository
from common.async_request import make_request
from common.database_connection import async_session
from common.config import settings
from models.dao.orm_models import Application
from models.dto.models import ApplicationModel, InputModel, ChangeModel
from datetime import datetime


async def check_and_create(data: InputModel):
    async with async_session() as session:
        application_repo = AbstractRepository[Application](session, Application)
        check = await application_repo.get_by_unique_field('agreement_id', data.agreement_id)
        if check is not None:
            return
        current_date = datetime.now()
        check = await application_repo.get_by_dict({"client_id": data.client_id,
                                                    "product_code": data.product_code})
        dates = []
        for c in check:
            dates.append(int(ApplicationModel.from_dao(c).create_date.timestamp()))

        application = Application.from_input(data)

        if len(dates) != 0:
            dates.sort(reverse=True)
            current_date = current_date.timestamp()
            if current_date - dates[0] <= settings.application_delay:
                application.status = "CLOSED"
                await make_request(host=settings.product_engine_host, port=settings.product_engine_port,
                                   end="agreement/{application.agreement_id}/update", method="post", data={'field': 'status',
                                                                                                           'value': 'CLOSED'})
        await application_repo.add(application)


async def get_new_applications():
    async with async_session() as session:
        application_repo = AbstractRepository[Application](session, Application)
        applications = await application_repo.get_by_field('status', 'NEW')
        return [x.id for x in applications]


async def update_application(data: dict):
    async with async_session() as session:
        application_repo = AbstractRepository[Application](session, Application)
        application = await application_repo.get_by_id(data["application_id"])
        application = await application_repo.update(application, data["field"], data["value"])
        return ApplicationModel.from_dao(application)
