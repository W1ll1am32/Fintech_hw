from common.abstract_repository import AbstractRepository
from common.database_connection import async_session
from models.dao.orm_models import Agreement
from models.dto.models import AgreementModel


async def update_agreement(data: dict):
    async with async_session() as session:
        agreement_repo = AbstractRepository[Agreement](session, Agreement)
        agreement = await agreement_repo.get_by_id(data["agreement_id"])
        if agreement is not None:
            if data["status"] == "APPROVED":
                agreement = await agreement_repo.update(agreement, "status", 'ACTIVE')
            else:
                agreement = await agreement_repo.update(agreement, "status", 'CLOSED')
            return AgreementModel.from_dao(agreement)
        return None


async def get_agreement_by_id(id: int):
    async with async_session() as session:
        agreement_repo = AbstractRepository[Agreement](session, Agreement)
        agreement = await agreement_repo.get_by_id(id)
        return agreement


async def get_new_agreements():
    async with async_session() as session:
        agreement_repo = AbstractRepository[Agreement](session, Agreement)
        agreements = await agreement_repo.get_by_field('status', 'NEW')
        return agreements
