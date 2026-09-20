import uuid
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from database import Base


class ProductModel(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    unit_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    stock_unit = Column(String, nullable=False, default="pcs")
    category_id = Column(String, ForeignKey("categories.category_id"), nullable=True)
    supplier_id = Column(String, ForeignKey("suppliers.supplier_id"), nullable=True)

    category = relationship("CategoryModel", back_populates="products")
    supplier = relationship("SupplierModel", back_populates="products")
    sale_items = relationship("SaleItemModel", back_populates="product")
