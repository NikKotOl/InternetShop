from app.models.userModel import UserModel
from app.repositories.userRepository import UserRepository
from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class UserService:

    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, id: int) -> UserModel:
        user = await self.user_repository.get_user_by_id(id=id)
        if user is None:
            raise UserNotFoundError(id)
        return user

    async def register_user(self, username: str, password: str) -> UserModel:
        user = await self.user_repository.get_user_by_username(username=username)

        if user is not None:
            raise UserAlreadyExistsError(username)

        password_hash = ph.hash(password)

        return await self.user_repository.add_user(
            username=username, password_hash=password_hash
        )

    async def authenticate_user(self, username: str, password: str) -> UserModel:
        user = await self.user_repository.get_user_by_username(username=username)

        if user is None:
            raise UserNotFoundError(username)

        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise InvalidCredentialsError()

        return user
