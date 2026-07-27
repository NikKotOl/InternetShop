from unittest.mock import Mock
import pytest

from app.models.categoryModel import CategoryModel
from app.models.productModel import ProductModel
from app.services.productService import ProductService
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository
from app.core.exceptions import CategoryNotFoundError, ProductNotFoundError


@pytest.fixture
def category_repository():
    return Mock(spec=CategoryRepository)


@pytest.fixture
def product_repository():
    return Mock(spec=ProductRepository)


@pytest.fixture
def product_service(
    category_repository: CategoryRepository, product_repository: ProductRepository
):
    return ProductService(product_repository, category_repository)


async def test_add_product_raises_category_not_found(
    category_repository, product_repository, product_service
):
    category_repository.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        await product_service.add_product("name", 999999)

    product_repository.add_product.assert_not_called()


async def test_add_product_success(
    category_repository, product_repository, product_service
):
    category_repository.get_category_by_id.return_value = CategoryModel(
        id=1, name="category_name"
    )
    product_repository.add_product.return_value = ProductModel(
        id=1, name="product_name", category_id=1
    )

    result = await product_service.add_product("product_name", 1)

    product_repository.add_product.assert_called_once_with(
        "product_name",
        1,
    )

    assert result.name == "product_name"
    assert result.category_id == 1


async def test_delete_product_raises_product_not_found(
    product_repository, product_service
):
    product_repository.get_product_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        await product_service.delete_product(99999)

    product_repository.delete_product.assert_not_called()


async def test_delete_product_success(product_repository, product_service):
    product = ProductModel(id=1, name="product_name", category_id=1)

    product_repository.get_product_by_id.return_value = product
    product_repository.delete_product.return_value = product

    result = await product_service.delete_product(1)

    product_repository.delete_product.assert_called_once_with(product)

    assert result.name == "product_name"
    assert result.id == 1
    assert result.category_id == 1


async def test_get_products_by_category_id_raises_category_not_found(
    category_repository, product_service
):
    category_repository.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        await product_service.get_products_by_category_id(1)


async def test_get_products_by_category_id_success(
    category_repository, product_repository, product_service
):
    products = [
        ProductModel(id=1, name="product1", category_id=1),
        ProductModel(id=2, name="product2", category_id=1),
        ProductModel(id=3, name="product3", category_id=1),
    ]

    category_repository.get_category_by_id.return_value = CategoryModel(
        id=1, name="category name"
    )
    product_repository.get_products_by_category_id.return_value = products[:3]

    result = await product_service.get_products_by_category_id(1)

    product_repository.get_products_by_category_id.assert_called_once_with(1)

    assert result == products
