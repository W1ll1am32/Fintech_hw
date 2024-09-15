from fastapi import APIRouter, Depends, HTTPException
from models.dto.models import SchedulePaymentModel
from services.schedule import ScheduleService
from typing import Annotated

schedule_router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)


@schedule_router.get("/{id}")
async def get_schedules_by_agreement_id(id: int, schedule_service: Annotated[ScheduleService, Depends()]) -> list[SchedulePaymentModel]:
    schedules = await schedule_service.get_schedules_by_agreement_id(id)
    if schedules is None:
        raise HTTPException(status_code=404, detail="No agreement by this id")
    return schedules


@schedule_router.get("/get/future")
async def get_future_schedules(schedule_service: Annotated[ScheduleService, Depends()]) -> list[SchedulePaymentModel]:
    schedules = await schedule_service.get_future_schedules
    if len(schedules) == 0:
        return []
    return [SchedulePaymentModel.from_dao(x) for x in schedules]
