from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.schema.ticket_schema import CreateTicket
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

    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket


def get_my_open_tickets(user: User, session: Session):
    return get_open_employee_tickets(user, session)


def get_user_ticket_by_id(id: int, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)
    validate_ticket_user(ticket, user)

    return ticket


def update_ticket_by_id(id: int, form: CreateTicket, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)
    validate_ticket_user(ticket, user)
    validate_ticket_not_assigned(ticket)

    ticket.title = form.title
    ticket.description = form.description
    ticket.priority = form.priority

    session.commit()
    session.refresh(ticket)

    return ticket


def delete_ticket_by_id(id: int, user: User, session: Session):
    ticket = get_ticket_by_id(id, session)
    validate_ticket_user(ticket, user)
    validate_ticket_not_assigned(ticket)

    session.delete(ticket)
    session.commit()

    return {"ok": f"ticket {id} deleted"}
