from typing import Optional

from app.models.base import BaseModel
from sqlmodel import Field, SQLModel


class UserBaseModel(SQLModel):
    first_name: str = Field(min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(min_length=1, max_length=50, description="User's last name")
    username: str = Field(min_length=3, max_length=255, unique=True, description="User's username")
    # email: str = Field(max_length=50, unique=True, description="User's email")
    password: str = Field(min_length=6, description="User's password")
    age: Optional[int] = Field(ge=0, description="User's age")
    address: Optional[str] = Field(default=None, description="User's address")


class User(BaseModel, UserBaseModel, table=True):
    pass


class UserCreate(UserBaseModel):
    pass
