from unittest.mock import Mock

import pytest

from app.core.dependencies import AsyncSession
from app.models.productModel import ProductModel
from app.repositories.productRepository import ProductRepository


@pytest.fixture
def session():
    return Mock(spec=AsyncSession)


@pytest.fixture
def product_repository(session):
    return ProductRepository(session=session)


async def test_get_products(session, product_repository):
    product1 = ProductModel(id=1, name="product1", category_id=1)
    product2 = ProductModel(id=2, name="product2", category_id=1)

    scalars_mock = Mock()
    scalars_mock.all.return_value = [product1, product2]

    execute_result_mock = Mock()
    execute_result_mock.scalars.return_value = scalars_mock

    session.execute.return_value = execute_result_mock

    result = await product_repository.get_products()

    assert result == [product1, product2]


async def test_delete_product(session, product_repository):
    product1 = ProductModel(id=1, name="product1", category_id=1)

    result = await product_repository.delete_product(product1)

    session.delete.assert_called_once_with(product1)
    session.commit.assert_called_once()

    assert result == product1


async def test_get_product_by_id(session, product_repository):
    product1 = ProductModel(id=1, name="product1", category_id=1)

    session.get.return_value = product1

    result = await product_repository.get_product_by_id(1)

    session.get.assert_called_once_with(ProductModel, 1)
    assert result == product1


async def test_get_products_by_category_id(session, product_repository):
    product1 = ProductModel(id=1, name="product1", category_id=1)
    product2 = ProductModel(id=2, name="product2", category_id=1)

    scalars_mock = Mock()
    scalars_mock.all.return_value = [product1, product2]

    execute_result_mock = Mock()
    execute_result_mock.scalars.return_value = scalars_mock

    session.execute.return_value = execute_result_mock

    result = await product_repository.get_products_by_category_id(1)

    session.execute.assert_called_once()
    assert result == [product1, product2]


async def test_add_product(session, product_repository):
    result = await product_repository.add_product("product1", 1)

    # Проверяем, что session.add был вызван с правильным объектом
    added_product = session.add.call_args[0][0]
    assert added_product.name == "product1"
    assert added_product.category_id == 1

    # Проверяем, что commit и refresh вызывались
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(added_product)

    # Проверяем, что вернулся тот же объект, который передавали в add/refresh
    assert result is added_product
    assert result.name == "product1"
    assert result.category_id == 1
