from common.abstract_repository import AbstractRepository
from common.database_connection import async_session
from models.dao.orm_models import SchedulePayment, Agreement
from numpy_financial import pmt, ppmt, ipmt
from models.dto.models import SchedulePaymentModel, AgreementModel
from functions.agreement import get_agreement_by_id
from datetime import datetime, timedelta, timezone


async def schedule_generation(interest: float, term: int, principal_amount: float) -> dict:
    schedule_dict = dict()
    for period in range(1, term + 1):
        principal_payment = round(float(ppmt(interest/1200.0, period, term, principal_amount)), 2)

        interest_payment = round(float(ipmt(interest/1200.0, period, term, principal_amount)), 2)

        schedule_dict[period] = -principal_payment, -interest_payment
    return schedule_dict


async def add_schedule(agreement_id: int):
    agreement = await get_agreement_by_id(agreement_id)
    agreement_model = AgreementModel.from_dao(agreement)
    schedule_dict = await schedule_generation(interest=agreement_model.interest, term=agreement_model.term,
                                              principal_amount=agreement_model.principal_amount)
    async with async_session() as session:
        schedule_repo = AbstractRepository[SchedulePayment](session, SchedulePayment)
        for key in schedule_dict:
            schedule_model = SchedulePaymentModel.init()
            schedule_model.agreement_id = agreement_id
            schedule_model.period = key
            schedule_model.payment_date = agreement_model.disbursement_datetime + timedelta(days=30 * key)
            schedule_model.principal_payment, schedule_model.interest_payment = schedule_dict[key]
            schedule_model.total_sum = -round(float(pmt(agreement_model.interest/1200.0, agreement_model.term, agreement_model.principal_amount)), 2)
            await schedule_repo.add(SchedulePayment.from_dto(schedule_model))


async def get_schedules_by_agreement_id(id: int):
    async with async_session() as session:
        schedule_repo = AbstractRepository[SchedulePayment](session, SchedulePayment)
        schedules = await schedule_repo.get_by_field('agreement_id', id)
        return [SchedulePaymentModel.from_dao(x) for x in schedules]


async def get_future_schedules():
    async with async_session() as session:
        schedule_repo = AbstractRepository[SchedulePayment](session, SchedulePayment)
        schedules = await schedule_repo.get_by_field('status', 'FUTURE')
        return [SchedulePaymentModel.from_dao(x) for x in schedules]


async def overdue_schedule(schedule_id: int):
    async with async_session() as session:
        schedule_repo = AbstractRepository[SchedulePayment](session, SchedulePayment)
        schedule = await schedule_repo.get_by_id(schedule_id)
        await schedule_repo.update(schedule, 'status', 'OVERDUE')


async def pay_schedule(data: dict):
    schedules = await get_schedules_by_agreement_id(data["agreement_id"])
    min_delta = timedelta.max
    date = datetime.fromisoformat(data["date"])
    schedule_id = -1
    for sch in schedules:
        if sch.status == 'FUTURE':
            sch_date = sch.payment_date.replace(tzinfo=timezone.utc)
            if sch_date > date:
                if sch_date - date < min_delta:
                    schedule_id = sch.id
                    min_delta = sch_date - date
    if schedule_id != -1:
        async with async_session() as session:
            schedule_repo = AbstractRepository[SchedulePayment](session, SchedulePayment)
            schedule = await schedule_repo.get_by_id(schedule_id)
            schedule_model = SchedulePaymentModel.from_dao(schedule)
            if data["payment"] == schedule_model.total_sum:
                await schedule_repo.update(schedule, 'status', 'PAID')


async def check_all_resolved(data: dict):
    schedules = await get_schedules_by_agreement_id(data["agreement_id"])
    check = True
    for sch in schedules:
        if sch.status == 'FUTURE':
            check = False
            break
    if check:
        async with async_session() as session:
            agreement_repo = AbstractRepository[Agreement](session, Agreement)
            agreement = await agreement_repo.get_by_id(data["agreement_id"])
            await agreement_repo.update(agreement, 'status', 'CLOSED')
