from unittest.mock import Mock

import pytest

from app.core.dependencies import AsyncSession
from app.core.exceptions import CategoryNotFoundError
from app.models.categoryModel import CategoryModel
from app.repositories.categoryRepository import CategoryRepository


@pytest.fixture
def session():
    return Mock(spec=AsyncSession)


@pytest.fixture
def category_repository(session):
    return CategoryRepository(session=session)


async def test_get_categories(session, category_repository):
    category1 = CategoryModel(id=1, name="name")
    category2 = CategoryModel(id=2, name="name")

    scalars_mock = Mock()
    scalars_mock.all.return_value = [category1, category2]

    execute_result_mock = Mock()
    execute_result_mock.scalars.return_value = scalars_mock

    session.execute.return_value = execute_result_mock

    result = await category_repository.get_categories()

    assert result == [category1, category2]


async def test_delete_category_success(session, category_repository):
    category = CategoryModel(id=1, name="name")
    session.get.return_value = category

    result = await category_repository.delete_category(1)

    session.delete.assert_called_once_with(category)
    session.commit.assert_called_once()

    assert result == category


async def test_delete_category_return_none(session, category_repository):
    session.get.return_value = None
    result = await category_repository.delete_category(id=10000000000)

    session.delete.assert_not_called()
    assert result is None


async def test_get_category_by_id(session, category_repository):
    category = CategoryModel(id=1, name="name")

    session.get.return_value = category

    result = await category_repository.get_category_by_id(1)

    session.get.assert_called_once_with(CategoryModel, 1)
    assert result == category


async def test_add_category(session, category_repository):
    result = await category_repository.add_category("name")

    added_category = session.add.call_args[0][0]
    assert added_category.name == "name"

    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(added_category)

    assert result is added_category
    assert result.name == "name"
