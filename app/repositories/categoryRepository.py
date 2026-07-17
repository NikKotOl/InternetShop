from typing import List, Optional

from app.models.categoryModels import CategoryModel
from app.db.database import AsyncSession


class CategoryRepository:

    def __init__(self, session:AsyncSession):
        ...

    async def get_categories(self) -> List[CategoryModel]:
        ...
    
    async def add_category(self, name:str) -> CategoryModel:
        ...
    
    async def delete_category(self, id:int) -> Optional[CategoryModel]:
        ...
