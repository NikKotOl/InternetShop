from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.userModel import UserModel
from app.repositories.userRepository import UserRepository
from app.services.userService import UserService

router = APIRouter()

@router.get("/users/", response_model=list[UserModel])
async def get_users(session: AsyncSession = Depends(get_db)):
    """Возвращает список всех пользователей из базы данных."""
    user_repository = UserRepository(session)
    return await user_repository.get_users()

@router.post("/users/", response_model=UserModel)
async def create_user(user: UserModel, session: AsyncSession = Depends(get_db)):
    """Создает нового пользователя в базе данных."""
    user_repository = UserRepository(session)
    return await user_repository.register_user(user)

@router.get("/users/{user_id}", response_model=UserModel)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
    """Возвращает пользователя по его идентификатору."""
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

