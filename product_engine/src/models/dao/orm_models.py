from typing import TYPE_CHECKING
from typing_extensions import Self
from datetime import date, datetime
from sqlalchemy import Integer, String, DateTime, Numeric, Date, Index, Column, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.database_connection import Base

if TYPE_CHECKING:
    from ..dto.models import ProductModel
    from ..dto.models import ClientModel
    from ..dto.models import AgreementModel
    from ..dto.models import SchedulePaymentModel


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    title: Mapped[int] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String, unique=True)
    min_term: Mapped[int] = mapped_column(Integer)
    max_term: Mapped[int] = mapped_column(Integer)
    min_interest: Mapped[int] = mapped_column(Integer)
    max_interest: Mapped[int] = mapped_column(Integer)
    min_principal_amount: Mapped[int] = mapped_column(Integer)
    max_principal_amount: Mapped[int] = mapped_column(Integer)
    min_origination_amount: Mapped[int] = mapped_column(Integer)
    max_origination_amount: Mapped[int] = mapped_column(Integer)

    @classmethod
    def from_dto(cls, product_model: 'ProductModel') -> Self:
        return Product(
            title=product_model.title,
            version=product_model.version,
            code=product_model.code,
            min_term=product_model.min_term,
            max_term=product_model.max_term,
            min_interest=product_model.min_interest,
            max_interest=product_model.max_interest,
            min_principal_amount=product_model.min_principal_amount,
            max_principal_amount=product_model.max_principal_amount,
            min_origination_amount=product_model.min_origination_amount,
            max_origination_amount=product_model.max_origination_amount
        )


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    second_name: Mapped[str] = mapped_column(String)
    third_name: Mapped[str] = mapped_column(String)
    birthday: Mapped[date] = mapped_column(Date)
    passport_number: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    salary: Mapped[int] = mapped_column(Integer)

    agreements: Mapped[list['Agreement']] = relationship('Agreement', back_populates='client', lazy='joined',
                                                         uselist=True)

    __table_args__ = (
        Index('first_name_index', 'first_name'),
        Index('second_name_index', 'second_name'),
        Index('third_name_index', 'third_name'),
    )

    @classmethod
    def from_dto(cls, client_model: 'ClientModel') -> Self:
        return Client(
            first_name=client_model.first_name,
            second_name=client_model.second_name,
            third_name=client_model.third_name,
            birthday=client_model.birthday,
            passport_number=client_model.passport_number,
            email=client_model.email,
            phone=client_model.phone,
            salary=client_model.salary
        )


class Agreement(Base):
    __tablename__ = "agreement"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    product_code: Mapped[str] = mapped_column(String)
    client_id: Mapped[int] = Column(Integer, ForeignKey('client.id'))
    term: Mapped[int] = mapped_column(Integer)
    interest: Mapped[float] = mapped_column(Float)
    principal_amount: Mapped[float] = mapped_column(Float)
    origination_amount: Mapped[float] = mapped_column(Float)
    disbursement_datetime: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String)

    product: Mapped['Product'] = relationship('Product', primaryjoin='Agreement.product_code==Product.code',
                                              foreign_keys=product_code, lazy='joined')

    client: Mapped['Client'] = relationship('Client', back_populates='agreements', lazy='subquery')

    @classmethod
    def from_dto(cls, agreement_model: 'AgreementModel') -> Self:
        return Agreement(
            product_code=agreement_model.product_code,
            client_id=agreement_model.client_id,
            term=agreement_model.term,
            interest=agreement_model.interest,
            principal_amount=agreement_model.principal_amount,
            origination_amount=agreement_model.origination_amount,
            disbursement_datetime=agreement_model.disbursement_datetime,
            status=agreement_model.status
        )


class SchedulePayment(Base):
    __tablename__ = "schedule_payment"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    agreement_id: Mapped[int] = Column(Integer, ForeignKey('agreement.id'))
    status: Mapped[str] = mapped_column(String)
    period: Mapped[int] = mapped_column(Integer)
    payment_date: Mapped[datetime] = mapped_column(DateTime)
    principal_payment: Mapped[float] = mapped_column(Float)
    interest_payment: Mapped[float] = mapped_column(Float)
    total_sum: Mapped[float] = mapped_column(Float)

    agreement: Mapped['Agreement'] = relationship('Agreement',
                                                primaryjoin='SchedulePayment.agreement_id==Agreement.id',
                                                foreign_keys=agreement_id, lazy='joined')

    @classmethod
    def from_dto(cls, schedule_payment_model: 'SchedulePaymentModel') -> Self:
        return SchedulePayment(
            agreement_id=schedule_payment_model.agreement_id,
            status=schedule_payment_model.status,
            period=schedule_payment_model.period,
            payment_date=schedule_payment_model.payment_date,
            principal_payment=schedule_payment_model.principal_payment,
            interest_payment=schedule_payment_model.interest_payment,
            total_sum=schedule_payment_model.total_sum
        )
