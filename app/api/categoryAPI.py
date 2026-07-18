from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.categoryRepository import CategoryRepository
from app.schemas.categorySchemas import CategoryCreateSchema, CategoryResponseSchema
from app.core.logger import logger

router = APIRouter(prefix="/categories", tags=["categories"])


def get_repository(session: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(session=session)


@router.get("/")
async def get_categories(
    repository: CategoryRepository = Depends(get_repository),
) -> Sequence[CategoryResponseSchema]:
    result = await repository.get_categories()
    logger.info("Get all categories")
    return [CategoryResponseSchema.model_validate(c) for c in result]


@router.post("/")
async def add_category(
    category: CategoryCreateSchema,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    result = await repository.add_category(category.name)
    logger.info(f"Category '{result.name}' (id={result.id}) was added")
    return CategoryResponseSchema.model_validate(result)


@router.delete("/{id}")
async def delete_category(
    id: int,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:

    result = await repository.delete_category(id=id)

    if result is None:
        logger.error(f"Category with id {id} not found")
        raise HTTPException(status_code=404, detail="Category not found")

    logger.info(f"Category with id {id} was deleted")
    return CategoryResponseSchema.model_validate(result)


@router.get("/{id}")
async def get_category_by_id(
    id: int,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    
    result = await repository.get_category_by_id(id=id)

    if result is None:
        logger.error(f"Category with id={id} not found")
        raise HTTPException(status_code=404, detail="Category not found")
    
    logger.info(f"Get category with id {id}")

    return CategoryResponseSchema.model_validate(result)
