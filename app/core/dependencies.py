from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.database import AsyncSessionLocal
from app.models.userModel import UserModel
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository
from app.repositories.userRepository import UserRepository
from app.services.productService import ProductService
from app.services.userService import UserService

http_bearer = HTTPBearer()


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


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session=session)


def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user_id = decode_access_token(credentials.credentials)
    user = await user_service.get_user_by_id(user_id)
    return user
