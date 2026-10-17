import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    category_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    products = relationship("ProductModel", back_populates="category")
