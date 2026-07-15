from help_desk_api.db.enum.history_actions import HistoryAction
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.ticket_history import TicketHistory
from help_desk_api.db.models.user import User


def create_ticket_history(
    _ticket: Ticket,
    _action: HistoryAction,
    _user: User,
    _old_value: str = "",
    _new_value: str = "",
) -> TicketHistory:
    new_ticket_history = TicketHistory(
        ticket=_ticket,
        action=_action,
        user=_user,
        old_value=_old_value,
        new_value=_new_value,
    )

    return new_ticket_history
