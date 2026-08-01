from typing import Sequence

from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_is_admin_user,
    get_current_user,
    get_product_repository,
    get_product_service,
)
from app.repositories.productRepository import ProductRepository
from app.schemas.productSchemas import ProductResponseSchema
from app.services.productService import ProductService
from app.core.logger import logger
from app.schemas.productSchemas import ProductCreateSchema

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"Description": "Product not found"}},
)


@router.get("/")
async def get_products(
    repository: ProductRepository = Depends(get_product_repository),
) -> Sequence[ProductResponseSchema]:
    result = await repository.get_products()
    logger.info("Get all products")
    return [ProductResponseSchema.model_validate(c) for c in result]


@router.get("/{product_id}")
async def get_product_by_id(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    result = await product_service.get_product_by_id(product_id)
    logger.info(f"Get product with id={product_id}")
    return ProductResponseSchema.model_validate(result)


@router.post("/", dependencies=[Depends(get_current_is_admin_user)])
async def add_product(
    product: ProductCreateSchema,
    product_service: ProductService = Depends(get_product_service),
) -> ProductResponseSchema:
    result = await product_service.add_product(product.name, product.category_id)
    logger.info(
        f"Added product with name={result.name}, category id={result.category_id} and id={result.id}"
    )
    return ProductResponseSchema.model_validate(result)


@router.delete("/{product_id}", dependencies=[Depends(get_current_is_admin_user)])
async def delete_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
) -> ProductResponseSchema:
    result = await product_service.delete_product(product_id)
    logger.info(f"Deleted product with id={product_id}")
    return ProductResponseSchema.model_validate(result)
