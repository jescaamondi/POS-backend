import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class SaleModel(Base):
    __tablename__ = "sales"

    sale_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    sale_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    sale_amount = Column(Numeric(10, 2), nullable=False)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    user = relationship("UserModel", back_populates="sales")
    customer = relationship("CustomerModel", back_populates="sales")
    sale_items = relationship("SaleItemModel", back_populates="sale", cascade="all, delete-orphan")
    payment = relationship("PaymentModel", back_populates="sale", uselist=False, cascade="all, delete-orphan")
    receipt = relationship("ReceiptModel", back_populates="sale", uselist=False, cascade="all, delete-orphan")
