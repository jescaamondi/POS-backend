import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class ReceiptModel(Base):
    __tablename__ = "receipts"

    receipt_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    sale_id = Column(String, ForeignKey("sales.sale_id"), nullable=False, unique=True)
    receipt_number = Column(String, nullable=False)
    issued_date = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    sale = relationship("SaleModel", back_populates="receipt")
