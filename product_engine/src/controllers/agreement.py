from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models.dto.models import AgreementModel, FormModel, ClientModel, ProductModel
from services.agreement import AgreementService

agreement_router = APIRouter(
    prefix="/agreement",
    tags=["agreement"],
)


@agreement_router.get("")
async def get_agreements(agreement_service: Annotated[AgreementService, Depends()]):
    agreements = await agreement_service.get_agreements()
    return agreements


@agreement_router.get("/{id}")
async def get_agreement_by_id(id: int, agreement_service: Annotated[AgreementService, Depends()]):
    agreement = await agreement_service.get_agreements_by_id(id)
    if agreement is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return agreement


@agreement_router.get("/client/{client_id}")
async def get_agreements_by_client_id(client_id: int, agreement_service: Annotated[AgreementService, Depends()]):
    agreements = await agreement_service.get_agreements_by_client_id(client_id)
    if agreements is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return agreements


@agreement_router.post("")
async def create_agreement(form: FormModel, agreement_service: Annotated[AgreementService, Depends()]) -> JSONResponse:
    id, client_id, code = await agreement_service.create_agreement(form)

    if code == 400:
        return JSONResponse(content={"message": "Data is out of range"}, status_code=400)
    if code == 404:
        return JSONResponse(content={"message": "Product not found"}, status_code=404)
    if code == 409:
        return JSONResponse(content={"message": "Conflict with client data. Check 'passport' field"}, status_code=409)
    return JSONResponse(content={"client_id": client_id, "agreement_id": id}, status_code=200)


@agreement_router.post("/{agreement_id}/close")
async def close_agreement(agreement_id: int, agreement_service: Annotated[AgreementService, Depends()]):
    r = await agreement_service.update_agreement({"agreement_id": agreement_id,
                                                "status": 'CLOSE',
                                                "field": "status"})
    if r is not None:
        return JSONResponse(content={"agreement_id": id}, status_code=200)
    else:
        return JSONResponse(content={"agreement_id": id}, status_code=404)
