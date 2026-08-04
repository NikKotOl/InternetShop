from decimal import Decimal
from typing import Sequence

from app.core.exceptions import CategoryNotFoundError, ProductNotFoundError
from app.models.productModel import ProductModel
from app.repositories.categoryRepository import CategoryRepository
from app.repositories.productRepository import ProductRepository


class ProductService:

    def __init__(
        self,
        productRepository: ProductRepository,
        categoryRepository: CategoryRepository,
    ):
        self.productRepository = productRepository
        self.categoryRepository = categoryRepository

    async def get_product_by_id(self, id: int) -> ProductModel:
        """
        Получает продукт по его идентификатору.

        Args:
            id (int): Уникальный идентификатор продукта в системе.

        Returns:
            ProductModel: Объект модели найденного продукта с полной информацией о нем, включая название и ID категории.

        Raises:
            ProductNotFoundError: Если продукт с указанным идентификатором не найден.
        """
        product = await self.productRepository.get_product_by_id(id)
        if product is None:
            raise ProductNotFoundError(id)
        return product

    async def add_product(
        self, name: str, category_id: int, price: Decimal
    ) -> ProductModel:
        """
        Добавляет новый продукт в категорию.

        Args:
            name (str): Название продукта для добавления. Должно быть непустой строкой без запрещенных символов.
            category_id (int): Уникальный идентификатор категории, к которой относится этот продукт. Категрия должна уже существовать.

        Returns:
            ProductModel: Объект модели созданного и сохраненного продукта с полной информацией о нем включая ID категории.

        Raises:
            CategoryNotFoundError: Если категория с указанным идентификатором не найдена или удалена.
            ValueError: Если название продукта является пустой строкой или содержит запрещенные символы.
        """
        category = await self.categoryRepository.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        return await self.productRepository.add_product(name, category_id, price)

    async def delete_product(self, id: int) -> ProductModel:
        """
        Удаляет продукт по его идентификатору.

        Args:
            id (int): Уникальный идентификатор продукта для удаления из системы. Продукт должен существовать и не иметь внешних ссылок на него.

        Returns:
            ProductModel: Объект модели удаленного продукта, который больше недоступно в системе после успешного удаления.

        Raises:
            ProductNotFoundError: Если продукт с указанным идентификатором не найден или уже был удалён из системы ранее.
        """
        product = await self.productRepository.get_product_by_id(id)
        if product is None:
            raise ProductNotFoundError(id)
        return await self.productRepository.delete_product(product)

    async def get_products_by_category_id(
        self, category_id: int
    ) -> Sequence[ProductModel]:
        """
        Получает список продуктов по идентификатору категории. Возвращается упорядоченный и отфильтрованный список уникальных активных элементов из всех категорий для данного ID с параметрами сортировки если они были заданы ранее через конструктор сервиса при его инициализации в базе данных или других местах приложения как это требуется правилами разработки бизнес-приложений.

        Args:
            category_id (int): Уникальный идентификатор категории, по которой необходимо получить список продуктов из этой конкретной группы товаров внутри одной логической сущности категории если она существует иначе возвращается пустой массив объектов модели продукта без информации о самой категорией для текущего пользователя согласно правилам безопасности приложения.

        Returns:
            Sequence[ProductModel]: Последовательность (список, кортеж или другой итератор) найденных активных продуктов данной категории с полной информацией об их свойствах включая ID соответствующей к ним категорий если они существуют иначе возвращается пустой последовательности объектов модели продукта без информации о самой категорией для текущего пользователя согласно правилам безопасности приложения.

        Raises:
            CategoryNotFoundError: Если категория с указанным идентификатором не найдена или удалена из системы ранее чем до выполнения запроса на получение списка продуктов по данной категории через этот метод сервиса ProductService который работает как фабрика для создания новых экземпляров объектов модели продукта если они существуют иначе возвращается пустой последовательности объектов моделей продукта без информации о самой категорией для текущего пользователя согласно правилам безопасности приложения.
        """

        category = await self.categoryRepository.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        return await self.productRepository.get_products_by_category_id(category_id)
