from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReceiptBase(BaseModel):
    sale_id: str
    receipt_number: str = Field(min_length=1)


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    sale_id: str | None = None
    receipt_number: str | None = Field(default=None, min_length=1)


class ReceiptRead(ReceiptBase):
    receipt_id: str
    issued_date: datetime
    model_config = ConfigDict(from_attributes=True)
