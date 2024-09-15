from pydantic import BaseModel
from datetime import date, datetime, timedelta


class ApplicationModel(BaseModel):
    product_code: str
    first_name: str
    second_name: str
    third_name: str
    birthday: str = datetime.now().strftime("%Y-%m-%d")
    passport_number: str = "0123456789"
    email: str = "email@email.com"
    phone: str = "88005553535"
    salary: int
    term: int = 5
    interest: float = 10
    disbursment_amount: float = 50001
