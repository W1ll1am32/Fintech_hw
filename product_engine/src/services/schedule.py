from fastapi import Depends
from models.dao.orm_models import SchedulePayment
from models.dto.models import SchedulePaymentModel
from common.repository_getter import get_repository
from datetime import timedelta, datetime, timezone
from services.agreement import AgreementService


class ScheduleService:
    def __init__(self, schedule_repo=Depends(get_repository(SchedulePayment)),
                 agreement_service: AgreementService = Depends(AgreementService)):
        self._schedule_repo = schedule_repo
        self._agreement_service = agreement_service

    async def get_future_schedules(self):
        schedules = await self._schedule_repo.get_by_field('status', 'FUTURE')
        return [SchedulePaymentModel.from_dao(x) for x in schedules]

    async def get_schedules_by_agreement_id(self, id: int):
        check = await self._agreement_service.get_agreements_by_id(id)
        if check is None:
            return None
        schedules = await self._schedule_repo.get_by_field('agreement_id', id)
        return [SchedulePaymentModel.from_dao(x) for x in schedules]

    async def pay_schedule(self, data: dict):
        schedules = await self._schedule_repo.get_by_field('agreement_id', data["agreement_id"])
        min_delta = timedelta.max
        date = datetime.fromisoformat(data["date"])
        schedule_id = -1
        for sch in schedules:
            sch_date = datetime.fromisoformat(sch["payment_date"])
            sch_date = sch_date.replace(tzinfo=timezone.utc)
            if sch_date > date:
                if sch_date - date < min_delta:
                    schedule_id = sch["id"]
                    min_delta = sch_date - date
        if schedule_id != -1:
            schedule = await self._schedule_repo.get_by_id(schedule_id)
            schedule_model = SchedulePaymentModel.from_dao(schedule)
            if data["payment"] == schedule_model.interest_payment + schedule_model.principal_payment:
                await self._schedule_repo.update(schedule, 'status', 'PAID')
