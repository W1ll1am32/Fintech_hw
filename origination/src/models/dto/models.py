from typing_extensions import Self
from pydantic import BaseModel
from models.dao.orm_models import Application
from datetime import datetime


class ApplicationModel(BaseModel):
    client_id: int
    disbursment_amount: int
    product_code: str
    agreement_id: int
    create_date: datetime
    status: str

    @classmethod
    def from_dao(cls, application_dao: Application) -> Self:
        return ApplicationModel(
            client_id=application_dao.client_id,
            disbursment_amount=application_dao.disbursment_amount,
            product_code=application_dao.product_code,
            agreement_id=application_dao.agreement_id,
            create_date=application_dao.create_date,
            status=application_dao.status
        )


class InputModel(BaseModel):
    client_id: int
    disbursment_amount: int
    agreement_id: int
    product_code: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return InputModel(
            client_id=data["client_id"],
            disbursment_amount=data["disbursment_amount"],
            agreement_id=data["agreement_id"],
            product_code=data["product_code"]
        )


class ChangeModel(BaseModel):
    field: str
    value: int | str


