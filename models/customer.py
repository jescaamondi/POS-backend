import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    customer_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    loyalty_points = Column(Integer, nullable=False, default=0)

    sales = relationship("SaleModel", back_populates="customer")
