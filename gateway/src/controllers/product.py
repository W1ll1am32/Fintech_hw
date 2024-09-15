from fastapi import HTTPException, APIRouter
from common.async_request import make_request
from common.config import settings


product_router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@product_router.get("")
async def get_all_products():
    data, status_code = await make_request(settings.product_engine_host, settings.product_engine_port, "product", "get")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return data


@product_router.get("/{code}")
async def get_product_by_code(code: str):
    data, status_code = await make_request(settings.product_engine_host, settings.product_engine_port, "product/{}".format(code), "get")
    if status_code == 404:
        raise HTTPException(status_code=404, detail="Not Found")
    if status_code == 408:
        raise HTTPException(status_code=408, detail="Request Timeout")
    if status_code == 503:
        raise HTTPException(status_code=503, detail="Service not available")
    return data
