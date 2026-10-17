import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    sale_item_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    sale_id = Column(String, ForeignKey("sales.sale_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    product_total = Column(Numeric(10, 2), nullable=False)

    sale = relationship("SaleModel", back_populates="sale_items")
    product = relationship("ProductModel", back_populates="sale_items")
