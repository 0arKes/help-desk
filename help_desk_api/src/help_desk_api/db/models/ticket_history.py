from datetime import datetime

from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.history_actions import HistoryAction
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from sqlalchemy import Enum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


@mapper_registry.mapped_as_dataclass
class TicketHistory:
    __tablename__ = "ticket_history"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, unique=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"), init=False)
    ticket: Mapped[Ticket] = relationship(back_populates="ticket_history")
    action: Mapped[HistoryAction] = mapped_column(Enum(HistoryAction))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    user: Mapped[User] = relationship(back_populates="ticket_history")

    old_value: Mapped[str] = mapped_column(Text)
    new_value: Mapped[str] = mapped_column(Text)

    performed_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False
    )
