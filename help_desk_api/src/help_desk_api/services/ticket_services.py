from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.exceptions.ticket_exceptions import (
    InvalidUserRole,
    TicketHasBeenAssigned,
)


def check_require_role(user_role: UserRole, allowed_role: UserRole):
    if user_role == allowed_role or user_role == UserRole.ADMIN:
        return

    raise InvalidUserRole()


def validate_ticket_not_assigned(ticket: Ticket):
    if ticket.responsible_id is not None:
        raise TicketHasBeenAssigned()
    return
