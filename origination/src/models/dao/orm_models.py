from typing import TYPE_CHECKING
from typing_extensions import Self
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKeyConstraint
from common.database_connection import Base
from datetime import datetime

if TYPE_CHECKING:
    from models.dto.models import ApplicationModel
    from models.dto.models import InputModel


class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer)
    disbursment_amount: Mapped[int] = mapped_column(Integer)
    product_code: Mapped[str] = mapped_column(String)
    agreement_id: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String)

    @classmethod
    def from_dto(cls, application_model: 'ApplicationModel') -> Self:
        return Application(
            client_id=application_model.client_id,
            disbursment_amount=application_model.disbursment_amount,
            product_code=application_model.product_code,
            agreement_id=application_model.agreement_id,
            create_date=application_model.create_date,
            status=application_model.status
        )

    @classmethod
    def from_input(cls, input_model: 'InputModel') -> Self:
        return Application(
            client_id=input_model.client_id,
            disbursment_amount=input_model.disbursment_amount,
            product_code=input_model.product_code,
            agreement_id=input_model.agreement_id,
            create_date=datetime.now(),
            status='NEW'
        )
