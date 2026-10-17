from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    phone_number: str | None = None
    loyalty_points: int = Field(default=0, ge=0)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1)
    last_name: str | None = Field(default=None, min_length=1)
    phone_number: str | None = None
    loyalty_points: int | None = Field(default=None, ge=0)


class CustomerRead(CustomerBase):
    customer_id: str
    model_config = ConfigDict(from_attributes=True)
