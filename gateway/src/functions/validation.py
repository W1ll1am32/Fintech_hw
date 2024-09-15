from fastapi import Response, APIRouter, HTTPException
from common.async_request import make_request
from common.config import settings
from models.dto.models import ApplicationModel
from datetime import datetime


def validate_data(form: ApplicationModel):
    if any(char.isdigit() for char in form.first_name) or any(char.isdigit() for char in form.second_name) or any(char.isdigit() for char in form.second_name):
        raise HTTPException(status_code=400, detail="Wrong name format")
    try:
        datetime.strptime(form.birthday, '%Y-%m-%d')
    except:
        raise HTTPException(status_code=400, detail="Wrong birthday format")
    if len(form.passport_number) != 10 and not form.passport_number.isnumeric():
        raise HTTPException(status_code=400, detail="Wrong passport format (10 numbers)")
    if '@' not in form.email:
        raise HTTPException(status_code=400, detail="Wrong email format")
    if not form.phone.isnumeric():
        raise HTTPException(status_code=400, detail="Wrong phone format")
