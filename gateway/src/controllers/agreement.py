from fastapi import Response, APIRouter, HTTPException
from common.async_request import make_request
from common.config import settings
from models.dto.models import ApplicationModel
from functions.validation import validate_data


agreement_router = APIRouter(
    prefix="/agreement",
    tags=["agreement"],
)


@agreement_router.post("")
async def create_agreement(form: ApplicationModel) -> Response:
    validate_data(form)
    data, status_code = await make_request(settings.product_engine_host, settings.product_engine_port, "agreement", "post", form.model_dump())
    if status_code == 400:
        raise HTTPException(status_code=400, detail="Data is out of range")
    if status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 409:
        raise HTTPException(status_code=409, detail="Conflict with client data. Check 'passport' field")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return data


@agreement_router.get("/{client_id}")
async def get_agreements_by_client_id(client_id: int) -> Response:
    data, status_code = await make_request(settings.product_engine_host, settings.product_engine_port, f"agreement/client/{client_id}", "get")
    if status_code == 404:
        raise HTTPException(status_code=404, detail="Client not found")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return data