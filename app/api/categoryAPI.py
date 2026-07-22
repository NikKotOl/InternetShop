from typing import Sequence

from fastapi import APIRouter, Depends

from app.core.dependencies import get_category_repository, get_product_service
from app.core.exceptions import CategoryNotFoundError
from app.repositories.categoryRepository import CategoryRepository
from app.schemas.categorySchemas import CategoryCreateSchema, CategoryResponseSchema
from app.core.logger import logger
from app.schemas.productSchemas import ProductResponseSchema
from app.services.productService import ProductService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
async def get_categories(
    repository: CategoryRepository = Depends(get_category_repository),
) -> Sequence[CategoryResponseSchema]:
    result = await repository.get_categories()
    logger.info("Get all categories")
    return [CategoryResponseSchema.model_validate(c) for c in result]


@router.post("/")
async def add_category(
    category: CategoryCreateSchema,
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryResponseSchema:
    result = await repository.add_category(category.name)
    logger.info(f"Category '{result.name}' (id={result.id}) was added")
    return CategoryResponseSchema.model_validate(result)


@router.delete("/{id}")
async def delete_category(
    id: int,
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryResponseSchema:

    result = await repository.delete_category(id=id)

    if result is None:
        logger.error(f"Category with id {id} not found")
        raise CategoryNotFoundError(id)

    logger.info(f"Category with id {id} was deleted")
    return CategoryResponseSchema.model_validate(result)


@router.get("/{id}")
async def get_category_by_id(
    id: int,
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryResponseSchema:

    result = await repository.get_category_by_id(id=id)

    if result is None:
        logger.error(f"Category with id={id} not found")
        raise CategoryNotFoundError(id)

    logger.info(f"Get category with id {id}")

    return CategoryResponseSchema.model_validate(result)


@router.get("/{category_id}/products")
async def get_products_by_category_id(
    category_id: int, product_service: ProductService = Depends(get_product_service)
) -> Sequence[ProductResponseSchema]:
    result = await product_service.get_products_by_category_id(category_id)
    logger.info(f"Get products with category id = {category_id}")
    return [ProductResponseSchema.model_validate(product) for product in result]
