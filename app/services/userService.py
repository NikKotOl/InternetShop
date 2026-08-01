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
        """Get user by their unique ID."""

        user = await self.user_repository.get_user_by_id(id=id)
        if user is None:
            raise UserNotFoundError(id)
        return user

    async def register_user(self, username: str, password: str) -> UserModel:
        """Register a new user account.

        :param username: The unique login name for the new user.
        :param password: The plain-text password to be hashed and stored securely.
        :return: A UserModel object containing the newly created user's data.
        :raises UserAlreadyExistsError: If a user with this username already exists.
        """

        user = await self.user_repository.get_user_by_username(username=username)

        if user is not None:
            raise UserAlreadyExistsError(username)

        password_hash = ph.hash(password)

        return await self.user_repository.add_user(
            username=username, password_hash=password_hash
        )

    async def authenticate_user(self, username: str, password: str) -> UserModel:
        """Authenticate a user with provided credentials.

        :param username: The login name of the user to authenticate.
        :param password: The plain-text password for verification.
        :return: A UserModel object containing authenticated user's data if successful.
        :raises UserNotFoundError: If no user exists with this username.
        :raises InvalidCredentialsError: If the provided credentials do not match.
        """

        user = await self.user_repository.get_user_by_username(username=username)

        if user is None:
            raise UserNotFoundError(username)

        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise InvalidCredentialsError()

        return user
