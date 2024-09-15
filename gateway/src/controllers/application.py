from fastapi import Response, APIRouter, HTTPException
from common.async_request import make_request
from common.config import settings

application_router = APIRouter(
    prefix="/application",
    tags=["application"],
)


@application_router.post("/{agreement_id}/close")
async def close_application(agreement_id: int) -> Response:
    data, status_code = await make_request(host=settings.origination_host, port=settings.origination_port, end=f"application/{agreement_id}/close", method="post")
    if status_code == 403:
        raise HTTPException(status_code=403, detail="The agreement is already active")
    if status_code == 404:
        raise HTTPException(status_code=404, detail="Application not found")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return Response(status_code=200)

