from fastapi import Depends
from models.dao.orm_models import Product
from models.dto.models import ProductModel
from common.repository_getter import get_repository


class ProductService:
    def __init__(self, product_repo=Depends(get_repository(Product))):
        self._product_repo = product_repo

    async def get_products(self):
        products = await self._product_repo.get_all()
        return [ProductModel.from_dao(x) for x in products]

    async def get_product_by_code(self, code: str):
        product = await self._product_repo.get_by_code(code)
        if product is not None:
            return ProductModel.from_dao(product)
        return None

    async def create_product(self, product: ProductModel):
        res = await self._product_repo.add(Product.from_dto(product))
        return res

    async def delete_product(self, code: str):
        await self._product_repo.delete_by_code(code)
