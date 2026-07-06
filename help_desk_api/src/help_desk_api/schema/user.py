from help_desk_api.db.enum.user_role import UserRole
from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole


class ReadUser(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
