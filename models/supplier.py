import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base


class SupplierModel(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    email_address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)

    products = relationship("ProductModel", back_populates="supplier")
