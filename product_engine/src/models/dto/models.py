from typing_extensions import Self
from pydantic import BaseModel
from ..dao.orm_models import Product, Client, Agreement, SchedulePayment
from datetime import date, datetime, timedelta


class FormModel(BaseModel):
    product_code: str
    first_name: str
    second_name: str
    third_name: str
    birthday: date
    passport_number: str = "0123456789"
    email: str = "email@email.com"
    phone: str = "88005553535"
    salary: int
    term: int = 5
    interest: float = 10
    disbursment_amount: float = 50001


class ScheduleInput(BaseModel):
    agreement_id: int


class PaymentInput(BaseModel):
    payment: float


class ProductModel(BaseModel):
    title: str
    version: int
    code: str
    min_term: int
    max_term: int
    min_interest: int
    max_interest: int
    min_principal_amount: int
    max_principal_amount: int
    min_origination_amount: int
    max_origination_amount: int

    @classmethod
    def from_dao(cls, product_dao: Product) -> Self:
        return ProductModel(
            title=product_dao.title,
            version=product_dao.version,
            code=product_dao.code,
            min_term=product_dao.min_term,
            max_term=product_dao.max_term,
            min_interest=product_dao.min_interest,
            max_interest=product_dao.max_interest,
            min_principal_amount=product_dao.min_principal_amount,
            max_principal_amount=product_dao.max_principal_amount,
            min_origination_amount=product_dao.min_origination_amount,
            max_origination_amount=product_dao.max_origination_amount
        )


class ClientModel(BaseModel):
    first_name: str
    second_name: str
    third_name: str
    birthday: date
    passport_number: str
    email: str
    phone: str
    salary: int

    @classmethod
    def from_dao(cls, product_dao: Client) -> Self:
        return ClientModel(
            first_name=product_dao.first_name,
            second_name=product_dao.second_name,
            third_name=product_dao.third_name,
            birthday=product_dao.birthday,
            passport_number=product_dao.passport_number,
            email=product_dao.email,
            phone=product_dao.phone,
            salary=product_dao.salary
        )

    @classmethod
    def from_form(cls, form: FormModel) -> Self:
        return ClientModel(
            first_name=form.first_name,
            second_name=form.second_name,
            third_name=form.third_name,
            birthday=form.birthday,
            passport_number=form.passport_number,
            email=form.email,
            phone=form.phone,
            salary=form.salary
        )


class AgreementModel(BaseModel):
    product_code: str
    client_id: int
    term: int
    interest: float
    principal_amount: float
    origination_amount: float
    disbursement_datetime: datetime
    status: str

    @classmethod
    def from_dao(cls, agreement_dao: Agreement) -> Self:
        return AgreementModel(
            product_code=agreement_dao.product_code,
            client_id=agreement_dao.client_id,
            term=agreement_dao.term,
            interest=agreement_dao.interest,
            principal_amount=agreement_dao.principal_amount,
            origination_amount=agreement_dao.origination_amount,
            disbursement_datetime=agreement_dao.disbursement_datetime,
            status=agreement_dao.status
        )

    @classmethod
    def from_form(cls, form: FormModel) -> Self:
        return AgreementModel(
            product_code=form.product_code,
            client_id=0,
            term=form.term,
            interest=form.interest,
            principal_amount=0,
            origination_amount=0,
            disbursement_datetime=datetime.now(),
            status='NEW'
        )


class SchedulePaymentModel(BaseModel):
    id: int
    agreement_id: int
    status: str
    period: int
    payment_date: datetime
    principal_payment: float
    interest_payment: float
    total_sum: float

    @classmethod
    def from_dao(cls, schedule_payment_dao: SchedulePayment) -> Self:
        return SchedulePaymentModel(
            id=schedule_payment_dao.id,
            agreement_id=schedule_payment_dao.agreement_id,
            status=schedule_payment_dao.status,
            period=schedule_payment_dao.period,
            payment_date=schedule_payment_dao.payment_date,
            principal_payment=schedule_payment_dao.principal_payment,
            interest_payment=schedule_payment_dao.interest_payment,
            total_sum=schedule_payment_dao.total_sum
        )

    @classmethod
    def init(cls) -> Self:
        return SchedulePaymentModel(
            id=0,
            agreement_id=0,
            status='FUTURE',
            period=0,
            payment_date=0,
            principal_payment=0.0,
            interest_payment=0.0,
            total_sum=0.0
        )
