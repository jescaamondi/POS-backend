from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    email: EmailStr
    role: str = Field(default="cashier", min_length=1)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1)
    last_name: str | None = Field(default=None, min_length=1)
    username: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    role: str | None = Field(default=None, min_length=1)
    password: str | None = Field(default=None, min_length=8)


class UserRead(UserBase):
    user_id: str
    model_config = ConfigDict(from_attributes=True)
