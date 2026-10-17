import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="cashier")
    is_active = Column(Boolean, nullable=False, default=True)

    sales = relationship("SaleModel", back_populates="user")
