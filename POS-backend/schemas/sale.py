from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    sale_amount: Decimal = Field(ge=0)
    customer_id: str | None = None
    user_id: str


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    sale_amount: Decimal | None = Field(default=None, ge=0)
    customer_id: str | None = None
    user_id: str | None = None


class SaleRead(SaleBase):
    sale_id: str
    sale_date: datetime
    model_config = ConfigDict(from_attributes=True)
