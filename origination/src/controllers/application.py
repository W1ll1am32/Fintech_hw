from fastapi import Depends, APIRouter, Response
from fastapi.responses import JSONResponse
from models.dto.models import ApplicationModel, InputModel, ChangeModel
from services.application import ApplicationService
from typing import Annotated

application_router = APIRouter(
    prefix="/application",
    tags=["application"],
)


@application_router.get("/new")
async def get_new_applications(application_service: Annotated[ApplicationService, Depends()]):
    applications = await application_service.get_new_applications()
    return applications


@application_router.get("")
async def get_applications(application_service: Annotated[ApplicationService, Depends()]) -> list[ApplicationModel]:
    applications = await application_service.get_applications()
    return applications


@application_router.post("/{agreement_id}/close")
async def close_application(agreement_id: int, application_service: Annotated[ApplicationService, Depends()]) -> Response:
    res = await application_service.close_application(agreement_id)
    if res == 403:
        return JSONResponse(content={"message": "The agreement is already active"}, status_code=403)
    if res == 404:
        return JSONResponse(content={"message": "Application not found"}, status_code=404)
    if res == 503:
        return JSONResponse(content={"message": "Service not available"}, status_code=503)
    return JSONResponse(content={"message": "Ok"}, status_code=200)
