from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository
from app.services.productService import ProductService


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_product_repository(
    session: AsyncSession = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(session=session)


def get_category_repository(
    session: AsyncSession = Depends(get_db),
) -> CategoryRepository:
    return CategoryRepository(session=session)


def get_product_service(
    productRepo: ProductRepository = Depends(get_product_repository),
    categoryRepo: CategoryRepository = Depends(get_category_repository),
) -> ProductService:
    return ProductService(productRepo, categoryRepo)
