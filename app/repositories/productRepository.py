from typing import Optional, Sequence

from sqlalchemy import select

from app.db.database import AsyncSession
from app.models.productModel import ProductModel


class ProductRepository:

    session: AsyncSession


    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_products(self) -> Sequence[ProductModel]:
        stmt = select(ProductModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    

    async def add_product(self, name:str, category_id:int) -> ProductModel:
        new_product = ProductModel(name=name, category_id=category_id)
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product
    

    async def delete_product(self, deleted_product: ProductModel) -> ProductModel:
        await self.session.delete(deleted_product)
        await self.session.commit()
        return deleted_product
    

    async def get_product_by_id(self, id:int) -> Optional[ProductModel]:
        return await self.session.get(ProductModel, id)
    

    async def get_products_by_category_id(self, id:int) -> Sequence[ProductModel]:
        stmt = select(ProductModel).where(ProductModel.category_id == id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
