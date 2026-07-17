from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.categoryRepository import CategoryRepository
from app.schemas.categorySchemas import CategoryCreateSchema, CategoryResponseSchema


router = APIRouter(prefix="/categories", tags=["categories"])


def get_repository(session: AsyncSession = Depends(get_db)) -> CategoryRepository:
    repository = CategoryRepository(session=session)
    return repository


@router.get("/")
async def get_categories(
    repository: CategoryRepository = Depends(get_repository),
) -> Sequence[CategoryResponseSchema]:
    ...


@router.post("/")
async def add_category(
    category: CategoryCreateSchema,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    ...


@router.delete("/{id}")
async def delete_category(
    id: int,
    repository: CategoryRepository = Depends(get_repository),
) -> CategoryResponseSchema:
    ...
