from sqlalchemy.exc import IntegrityError
from typing import Optional, Sequence

from app.core.exceptions import CategoryAlreadyExistsError
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
            AlreadyExistsError: If a category with this name already exists.
        """
        new_category = CategoryModel(name=name)
        self.session.add(new_category)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise CategoryAlreadyExistsError(name)
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
