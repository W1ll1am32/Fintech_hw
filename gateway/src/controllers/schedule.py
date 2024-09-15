from fastapi import Response, APIRouter, HTTPException
from common.async_request import make_request
from common.config import settings


schedule_router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)


@schedule_router.get("/{agreement_id}")
async def get_schedule(agreement_id: int) -> Response:
    data, status_code = await make_request(settings.product_engine_host, settings.product_engine_port, f"schedule/{agreement_id}", "get")
    if status_code == 404:
        raise HTTPException(status_code=404, detail="No agreement by this id")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return data
