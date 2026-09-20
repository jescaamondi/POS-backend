from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    sale_id: str
    payment_method: str = Field(min_length=1)
    amount: Decimal = Field(ge=0)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    sale_id: str | None = None
    payment_method: str | None = Field(default=None, min_length=1)
    amount: Decimal | None = Field(default=None, ge=0)


class PaymentRead(PaymentBase):
    payment_id: str
    payment_date: datetime
    model_config = ConfigDict(from_attributes=True)
