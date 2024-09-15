from sqlalchemy.ext.asyncio import AsyncSession
from common.abstract_repository import AbstractRepository
from common.database_connection import get_session
from fastapi import Depends


def get_repository(table_cls):
    def get_repo(session: AsyncSession = Depends(get_session)):
        return AbstractRepository(session, table_cls)

    return get_repo
