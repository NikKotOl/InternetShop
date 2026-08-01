from typing import Optional, Sequence

from app.core.exceptions import CategoryNotFoundError
from app.models.categoryModel import CategoryModel
from app.db.database import AsyncSession

from sqlalchemy import select


class CategoryRepository:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories(self) -> Sequence[CategoryModel]:
        """Retrieve all categories from the database."""
        stmt = select(CategoryModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_category(self, name: str) -> CategoryModel:
        """Add a new category to the database.

        Args:
            name (str): The name of the category to be added.

        Returns:
            CategoryModel: The newly created and saved category instance.

        Raises:
            Exception: If an error occurs during save/commit (not explicitly raised in original, but good practice).
        """
        new_category = CategoryModel(name=name)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

    async def delete_category(self, id: int) -> Optional[CategoryModel]:
        deleted_category = await self.session.get(CategoryModel, id)
        if deleted_category:
            await self.session.delete(deleted_category)
            await self.session.commit()
            return deleted_category
        else:
            return None

    async def get_category_by_id(self, id: int) -> Optional[CategoryModel]:
        return await self.session.get(CategoryModel, id)
