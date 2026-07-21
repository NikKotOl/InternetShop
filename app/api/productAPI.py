from typing import Sequence

from fastapi import APIRouter, Depends

from app.core.dependencies import get_product_repository, get_product_service
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository
from app.schemas.productSchemas import ProductResponseSchema
from app.services.productService import ProductService
from app.core.logger import logger
from app.schemas.productSchemas import ProductCreateSchema


router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/")
async def get_products(
    repository: ProductRepository = Depends(get_product_repository),
) -> Sequence[ProductResponseSchema]:
    result = await repository.get_products()
    logger.info("Get all products")
    return [ProductResponseSchema.model_validate(c) for c in result]


@router.post("/")
async def add_product(
    product: ProductCreateSchema, product_service: ProductService = Depends(get_product_service)
) -> ProductResponseSchema:
    result = await product_service.add_product(product.name, product.category_id)
    logger.info(f"Added product with name={result.name}, category id={result.category_id} and id={result.id}")
    return ProductResponseSchema.model_validate(result)


@router.delete("/{id}")
async def delete_product(
    id: int, product_service: ProductService = Depends(get_product_service)
) -> ProductResponseSchema:
    result = await product_service.delete_product(id)
    logger.info(f"Deleted product with id={id}")
    return ProductResponseSchema.model_validate(result)
