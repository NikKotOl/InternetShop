from typing import Optional

from sqlalchemy import select

from app.db.database import AsyncSession
from app.models.userModel import UserModel


class UserRepository:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.username == username)
        user = await self.session.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_id(self, id: int) -> Optional[UserModel]:
        user = await self.session.get(UserModel, id)
        return user

    async def add_user(self, username: str, password_hash: str) -> UserModel:
        new_user = UserModel(username=username, password_hash=password_hash)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
