from help_desk_api.db.enum.history_actions import HistoryAction
from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.schema.ticket_schema import CreateTicket
from help_desk_api.services.history import create_ticket_history
from help_desk_api.services.ticket_core_services import (
    get_open_employee_tickets,
    get_ticket_by_id,
    validate_require_role,
    validate_ticket_not_assigned,
    validate_ticket_user,
)
from sqlalchemy.orm import Session


def create_ticket(form: CreateTicket, user: User, session: Session):

    validate_require_role(user.role, UserRole.EMPLOYEE)

    new_ticket = Ticket(
        title=form.title,
        description=form.description,
        creator=user,
        priority=form.priority,
        responsible_id=None,
    )
    history = create_ticket_history(
        new_ticket,
        HistoryAction.CREATED,
        user,
    )

    session.add(new_ticket)
    session.add(history)
    session.commit()
    session.refresh(new_ticket)
    session.refresh(history)
    return new_ticket


def get_my_open_tickets(user: User, session: Session):
    return get_open_employee_tickets(user, session)


def get_user_ticket_by_id(id: int, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)

    return ticket


def update_ticket_by_id(id: int, form: CreateTicket, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)
    validate_ticket_user(ticket, user)
    validate_ticket_not_assigned(ticket)

    history = create_ticket_history(
        ticket,
        HistoryAction.UPDATED,
        user,
        _old_value=(
            f"title={ticket.title}; "
            f"description={ticket.description}; "
            f"priority={ticket.priority.value}"
        ),
        _new_value=(
            f"title={form.title}; "
            f"description={form.description}; "
            f"priority={form.priority.value}"
        ),
    )

    ticket.title = form.title
    ticket.description = form.description
    ticket.priority = form.priority

    session.add(history)
    session.commit()
    session.refresh(ticket)

    return ticket


def delete_ticket_by_id(id: int, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)
    validate_ticket_user(ticket, user)
    validate_ticket_not_assigned(ticket)

    ticket.status = TicketStatus.DELETED
    session.commit()

    return {"ok": f"ticket {id} deleted"}
