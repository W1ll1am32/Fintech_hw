from fastapi import Depends
from common.repository_getter import get_repository
from common.async_request import make_request
from common.config import settings
from models.dao.orm_models import Application
from kafka.producer import get_producer
from models.dto.models import ApplicationModel, InputModel, ChangeModel


class ApplicationService:
    def __init__(self, application_repo=Depends(get_repository(Application)),
                 producer=Depends(get_producer)):
        self._application_repo = application_repo
        self._producer = producer

    async def get_applications(self):
        applications = await self._application_repo.get_all()
        return [ApplicationModel.from_dao(x) for x in applications]

    async def get_new_applications(self):
        applications = await self._application_repo.get_by_field('status', 'NEW')
        return [ApplicationModel.from_dao(x) for x in applications]

    async def get_applications_by_id(self, id: int):
        application = await self._application_repo.get_by_id(id)
        if application is not None:
            return ApplicationModel.from_dao(application)
        return None

    async def close_application(self, agreement_id: int):
        application = await self._application_repo.get_by_unique_field('agreement_id', agreement_id)
        print(application)
        if application is not None:
            try:
                data, _ = await make_request(host=settings.product_engine_host, port=settings.product_engine_port,
                                             end=f"schedule/get/future", method="get")
                if len(data) == 0:
                    _, status_code = await make_request(host=settings.product_engine_host, port=settings.product_engine_port,
                                                        end=f"agreement/{agreement_id}/close", method="post")
                    return 200
                else:
                    return 403
            except ConnectionError as e:
                return 503
        return 404
