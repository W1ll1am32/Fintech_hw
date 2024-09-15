from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.client import ClientService

client_router = APIRouter(
    prefix="/client",
    tags=["client"],
)


@client_router.get("")
async def get_clients(client_service: Annotated[ClientService, Depends()]):
    clients = await client_service.get_clients()
    return clients


@client_router.get("/{id}")
async def get_client_by_id(id: int, client_service: Annotated[ClientService, Depends()]):
    client = await client_service.get_client_by_id(id)
    if client is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return client
