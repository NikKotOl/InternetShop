from typing import Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.categoryRepository import CategoryRepository
from app.schemas.categorySchemas import CategoryCreateSchema, CategoryResponseSchema

router = APIRouter(prefix="/categories", tags=["categories"])


def get_repository(session: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(session=session)


@router.get("/")
async def get_categories(
    repository: CategoryRepository = Depends(get_repository),
) -> Sequence[CategoryResponseSchema]:
    return await repository.get_categories()  # type: ignore


@router.post("/")
async def add_category(
    category: CategoryCreateSchema,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    return await repository.add_category(category.name)  # type: ignore


@router.delete("/{id}")
async def delete_category(
    id: int,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:

    result = await repository.delete_category(id=id)

    if result is not None:
        return result  # type: ignore

    raise HTTPException(status_code=404, detail="Category not found")


@router.get("/{id}")
async def get_category_by_id(
    id: int,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    result = await repository.get_category_by_id(id=id)

    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return result  # type: ignore
