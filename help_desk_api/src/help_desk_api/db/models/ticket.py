from datetime import datetime

from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.ticket_priority import TicketPriority
from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.models.user import User
from sqlalchemy import Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


@mapper_registry.mapped_as_dataclass
class Ticket:
    __tablename__ = "ticket"
    id: Mapped[int] = mapped_column(
        primary_key=True, init=False, unique=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped[User] = relationship(
        back_populates="created_tickets", foreign_keys=[creator_id], init=False
    )

    responsible_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    responsible: Mapped[User | None] = relationship(
        back_populates="responsible_tickets", foreign_keys=[responsible_id], init=False
    )

    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.OPEN
    )
    priority: Mapped[TicketPriority] = mapped_column(
        Enum(TicketPriority), default=TicketPriority.NORMAL
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
