import pytest
from sqlalchemy import text
from testcontainers.community.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from app.core.dependencies import get_db
from app.core.security import create_access_token
from app.db.base import Base
from app.models.userModel import UserModel
from main import application


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        yield postgres.get_connection_url()


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    async_url = postgres_container.replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://"
    )
    return create_async_engine(url=async_url)


@pytest.fixture(scope="session")
def test_async_session(test_engine):
    return async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest.fixture(scope="session", autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def override_get_db(test_async_session):
    async def _get_test_db():
        async with test_async_session() as session:
            yield session

    application.dependency_overrides[get_db] = _get_test_db
    yield
    application.dependency_overrides.clear()


@pytest.fixture
async def client(override_get_db):
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def cleanup_database(test_engine):
    yield

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest.fixture(scope="function")
async def admin_token(test_async_session, cleanup_database) -> str:
    async with test_async_session() as session:
        user = UserModel(
            username="test_admin",
            password_hash="fake_hash_not_used_for_login",
            is_admin=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return create_access_token(user.id)
