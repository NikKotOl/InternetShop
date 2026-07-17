from typing import Optional, Sequence

from app.models.categoryModels import CategoryModel
from app.db.database import AsyncSession

from sqlalchemy import select


class CategoryRepository:

    session: AsyncSession

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_categories(self) -> Sequence[CategoryModel]:
        stmt = select(CategoryModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def add_category(self, name:str) -> CategoryModel:
        new_category = CategoryModel(name=name)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category
    
    async def delete_category(self, id:int) -> Optional[CategoryModel]:
        deleted_category = await self.session.get(CategoryModel, id)
        if deleted_category:
            await self.session.delete(deleted_category)
            await self.session.commit()
            return deleted_category
        else:
            return None
        
    async def get_category_by_id(self, id: int) -> Optional[CategoryModel]:
        category = await self.session.get(CategoryModel, id)
        return category
