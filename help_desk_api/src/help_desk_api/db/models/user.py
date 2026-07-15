from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.user_role import UserRole
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, init=False, unique=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), name="user_role")

    created_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="creator", init=False, foreign_keys="Ticket.creator_id"
    )
    responsible_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="responsible", init=False, foreign_keys="Ticket.responsible_id"
    )

    ticket_history: Mapped[list["TicketHistory"]] = relationship(
        back_populates="user", init=False
    )
