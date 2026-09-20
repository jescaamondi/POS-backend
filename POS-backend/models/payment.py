import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class PaymentModel(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    sale_id = Column(String, ForeignKey("sales.sale_id"), nullable=False, unique=True)
    payment_method = Column(String, nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    amount = Column(Numeric(10, 2), nullable=False)

    sale = relationship("SaleModel", back_populates="payment")
