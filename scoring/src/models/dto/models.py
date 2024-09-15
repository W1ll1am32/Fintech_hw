from typing_extensions import Self
from pydantic import BaseModel
from datetime import datetime


class AgreementModel(BaseModel):
    product_code: str
    client_id: int
    term: int
    interest: int
    principal_amount: int
    origination_amount: int
    create_datetime: datetime
    status: str


class InputModel(BaseModel):
    application_id: int
    client_id: int
    agreement_id: int
