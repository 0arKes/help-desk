from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.exceptions.ticket_exceptions import TicketNotFound
from help_desk_api.schema.ticket_schema import CreateTicket
from help_desk_api.services.ticket_services import (
    check_require_role,
    validate_ticket_not_assigned,
)
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

### Create


def create_ticket(form: CreateTicket, user: User, session: Session):

    check_require_role(user.role, UserRole.EMPLOYEE)

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


def update_ticket(id: int, form: CreateTicket, user: User, session: Session):
    ticket = get_tickets_by_id(id, user, session)

    validate_ticket_not_assigned(ticket)

    ticket.title = form.title
    ticket.description = form.description
    ticket.priority = form.priority

    session.commit()
    session.refresh(ticket)

    return ticket


def delete_ticket(id: int, user: User, session: Session):
    ticket = get_tickets_by_id(id, user, session)

    validate_ticket_not_assigned(ticket)

    session.delete(ticket)
    session.commit()

    return {"ok": f"ticket {id} deleted"}


### GET


def get_my_tickets(user: User, session: Session):

    tickets = session.scalars(
        select(Ticket)
        .where(Ticket.creator_id == user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    ).all()
    return {"tickets": tickets}


def get_tickets_by_id(id: int, user: User, session: Session):

    ticket = session.scalar(
        select(Ticket)
        .where(Ticket.id == id)
        .where(Ticket.creator_id == user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )
    if not ticket:
        raise TicketNotFound()
    return ticket


### Technician responsible
def queue_without_responsible(user: User, session: Session):
    check_require_role(user.role, UserRole.TECHNICIAN)
    queue = session.scalars(select(Ticket).where(Ticket.responsible_id == None)).all()
    return {"tickets": queue}
