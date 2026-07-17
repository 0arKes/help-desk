from help_desk_api.db.enum.user_role import UserRole
from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    name: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole


class ReadUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole


class UpdateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class CreateAdminUser(BaseModel):
    name: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=6)
