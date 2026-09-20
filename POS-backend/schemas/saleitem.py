from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    sale_id: str
    product_id: str
    quantity: int = Field(gt=0)
    product_total: Decimal = Field(ge=0)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    sale_id: str | None = None
    product_id: str | None = None
    quantity: int | None = Field(default=None, gt=0)
    product_total: Decimal | None = Field(default=None, ge=0)


class SaleItemRead(SaleItemBase):
    sale_item_id: str
    model_config = ConfigDict(from_attributes=True)
