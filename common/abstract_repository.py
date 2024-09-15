import datetime
from typing import Sequence, Iterable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import and_, cast, BOOLEAN
from typing import TypeVar, Generic, Optional, List, Type
from .database_connection import Base

T = TypeVar("T", bound=Base)


class AbstractRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session: AsyncSession = session
        self._table_cls: T = model_cls

    async def get_all(self) -> Sequence[T]:
        result = await self._session.execute(select(self._table_cls))
        return result.scalars().all()

    async def get_all_unique(self) -> Sequence[T]:
        result = await self._session.execute(select(self._table_cls))
        return result.scalars().unique().all()

    async def get_by_code(self, code: str) -> T | None:
        result = await self._session.execute(select(self._table_cls).where(self._table_cls.code == code))
        return result.scalars().one_or_none()

    async def get_by_id(self, id: int | UUID) -> T | None:
        result = await self._session.execute(select(self._table_cls).where(self._table_cls.id == id))
        return result.scalars().one_or_none()

    async def get_by_id_unique(self, id: int | UUID) -> T | None:
        result = await self._session.execute(select(self._table_cls).where(self._table_cls.id == id))
        return result.scalars().unique().one_or_none()

    async def get_by_list(self, data: list) -> bool:
        z = zip(self._table_cls.__table__.columns.keys()[1:], data)
        result = await self._session.execute(
            select(self._table_cls).where(and_(*[getattr(self._table_cls, c) == d for c, d in z])))
        return result.unique().scalars().one_or_none()

    async def get_by_dict(self, data: dict) -> Sequence[T]:
        result = await self._session.execute(
            select(self._table_cls).where(and_(getattr(self._table_cls, k) == v for k, v in data.items())))
        return result.scalars().all()

    async def add(self, table_cls: T) -> T | None:
        self._session.add(table_cls)
        await self._session.commit()
        await self._session.refresh(table_cls)
        return table_cls

    async def delete(self, table_cls: T) -> None:
        await self._session.delete(table_cls)
        await self._session.commit()

    async def delete_by_code(self, code: str) -> None:
        record = await self.get_by_code(code)
        if record is not None:
            await self._session.delete(record)
            await self._session.commit()

    async def delete_by_id(self, id: int) -> int:
        record = await self.get_by_id(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.commit()
            return 1
        else:
            return 0

    async def get_by_field(self, field: str, value: int | str) -> Sequence[T]:
        result = await self._session.execute(
            select(self._table_cls).where(cast(getattr(self._table_cls, field) == value, BOOLEAN)))
        return result.scalars().all()

    async def get_by_unique_field(self, field: str, value: int | str) -> T | None:
        result = await self._session.execute(
            select(self._table_cls).where(cast(getattr(self._table_cls, field) == value, BOOLEAN)))
        return result.scalars().one_or_none()
    
    async def update(self, table_cls: T, field: str, value: int | str | datetime.datetime) -> T:
        setattr(table_cls, field, value)
        await self._session.commit()
        await self._session.refresh(table_cls)
        return table_cls
