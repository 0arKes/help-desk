from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.user_role import UserRole
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, unique=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), name="user_role")
