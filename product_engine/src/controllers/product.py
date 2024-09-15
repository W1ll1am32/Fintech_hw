from fastapi import APIRouter, Depends, HTTPException, Response
from models.dto.models import ProductModel
from services.product import ProductService
from typing import Annotated


product_router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@product_router.get("")
async def get_all_products(product_service: Annotated[ProductService, Depends()]):
    products = await product_service.get_products()
    return products


@product_router.get("/{code}")
async def get_product_by_code(code: str, product_service: Annotated[ProductService, Depends()]):
    product = await product_service.get_product_by_code(code)
    if product is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return product


@product_router.post("")
async def create_product(product: ProductModel, product_service: Annotated[ProductService, Depends()]):
    res = await product_service.create_product(product)
    if res is None:
        return Response(status_code=409)
    return Response(status_code=200)


@product_router.delete("/{code}")
async def delete_product(code: str, product_service: Annotated[ProductService, Depends()]) -> Response:
    await product_service.delete_product(code)
    return Response(status_code=204)
