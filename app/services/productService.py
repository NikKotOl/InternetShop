from typing import Optional

from app.core.exceptions import CategoryNotFoundError
from app.models.productModel import ProductModel
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository


class ProductService:

    def __init__(self, productRepository: ProductRepository, categoryRepository: CategoryRepository):
        self.productRepository = productRepository
        self.categoryRepository = categoryRepository
    

    async def add_product(self, name: str, category_id: int) -> ProductModel:
        category = await self.categoryRepository.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        return await self.productRepository.add_product(name, category_id)
