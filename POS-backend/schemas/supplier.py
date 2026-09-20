from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBase(BaseModel):
    name: str = Field(min_length=1)
    email_address: EmailStr
    phone_number: str = Field(min_length=1)
    address: str = Field(min_length=1)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email_address: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=1)
    address: str | None = Field(default=None, min_length=1)


class SupplierRead(SupplierBase):
    supplier_id: str
    model_config = ConfigDict(from_attributes=True)
