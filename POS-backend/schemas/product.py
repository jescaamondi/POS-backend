from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    unit_price: Decimal = Field(ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    stock_unit: str = Field(default="pcs", min_length=1)
    category_id: str | None = None
    supplier_id: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    unit_price: Decimal | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    stock_unit: str | None = Field(default=None, min_length=1)
    category_id: str | None = None
    supplier_id: str | None = None


class ProductRead(ProductBase):
    product_id: str
    model_config = ConfigDict(from_attributes=True)
