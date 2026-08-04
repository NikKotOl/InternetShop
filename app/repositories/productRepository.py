from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import select

from app.db.database import AsyncSession
from app.models.productModel import ProductModel


class ProductRepository:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        """Initializes the product repository with a database session.
        Args:
            session: An asynchronous SQLAlchemy session for database operations.
        """
        self.session = session

    async def get_products(self) -> Sequence[ProductModel]:
        """Retrieves all products from the database.
        Returns:
            A sequence of ProductModel objects representing all products.
        """
        stmt = select(ProductModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_product(
        self, name: str, category_id: int, price: Decimal
    ) -> ProductModel:
        """Adds a new product to the database.
        Args:
            name: The name of the product.
            category_id: The identifier of the category to which the product belongs.
        Returns:
            The saved ProductModel object with an assigned identifier.
        """
        new_product = ProductModel(name=name, category_id=category_id, price=price)
        self.session.add(new_product)
        await self.session.flush()
        await self.session.refresh(new_product)
        return new_product

    async def delete_product(self, deleted_product: ProductModel) -> ProductModel:
        """Deletes a product from the database.
        Args:
            deleted_product: The ProductModel object to be deleted.

        Returns:
            The deleted ProductModel object.
        """
        await self.session.delete(deleted_product)
        return deleted_product

    async def get_product_by_id(self, id: int) -> Optional[ProductModel]:
        """Retrieves a product by its identifier.
        Args:
            id: The identifier of the product.
        Returns:
            The ProductModel object if found, otherwise None.
        """
        return await self.session.get(ProductModel, id)

    async def get_products_by_category_id(
        self, category_id: int
    ) -> Sequence[ProductModel]:
        """Retrieves all products belonging to the specified category.
        Args:
            category_id: The identifier of the category.
        Returns:
            A sequence of ProductModel objects belonging to the category.
        """
        stmt = select(ProductModel).where(ProductModel.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
