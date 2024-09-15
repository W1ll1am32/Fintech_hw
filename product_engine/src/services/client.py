from fastapi import APIRouter, Depends, HTTPException, Response
from models.dao.orm_models import Agreement, Client, Product
from models.dto.models import AgreementModel, FormModel, ClientModel, ProductModel
from common.repository_getter import get_repository


class ClientService:
    def __init__(self, client_repo=Depends(get_repository(Client))):
        self._client_repo = client_repo

    async def get_clients(self):
        clients = await self._client_repo.get_all_unique()
        return [(f"Client id: {x.id}", ClientModel.from_dao(x)) for x in clients]

    async def get_client_by_id(self, id: int):
        client = await self._client_repo.get_by_id_unique(id)
        if client is not None:
            return ClientModel.from_dao(client)
        return None

    async def get_and_create(self, list, form):
        client = await self._client_repo.get_by_list(list)
        if client is None:
            client = Client.from_dto(ClientModel.from_form(form))
            await self._client_repo.add(client)
        return client
