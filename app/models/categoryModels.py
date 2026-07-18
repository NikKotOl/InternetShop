from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    products: Mapped[list["ProductModel"]] = relationship()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


if TYPE_CHECKING:
    from app.models.productModels import ProductModel
