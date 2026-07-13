from help_desk_api.db.enum.ticket_priority import TicketPriority
from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.exceptions.ticket_exceptions import (
    InvalidTicketStatus,
    TicketDoesNotBelongToUser,
    TicketNotFound,
)
from help_desk_api.schema.ticket_schema import CreateTicket
from help_desk_api.services.ticket_services import (
    check_require_role,
    validate_ticket_not_assigned,
)
from sqlalchemy import case, select
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
    ticket = get_user_ticket_by_id(id, user, session)

    validate_ticket_not_assigned(ticket)

    ticket.title = form.title
    ticket.description = form.description
    ticket.priority = form.priority

    session.commit()
    session.refresh(ticket)

    return ticket


def delete_ticket(id: int, user: User, session: Session):
    ticket = get_user_ticket_by_id(id, user, session)

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


def get_user_ticket_by_id(id: int, user: User, session: Session):

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


def get_ticket_by_id(id: int, session: Session, validation_assigned=True):

    ticket = session.scalar(
        select(Ticket)
        .where(Ticket.id == id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )
    if not ticket:
        raise TicketNotFound()

    if validation_assigned:
        validate_ticket_not_assigned(ticket)

    return ticket


def queue_without_responsible(user: User, session: Session):
    check_require_role(user.role, UserRole.TECHNICIAN)

    priority_order = case(
        (Ticket.priority == TicketPriority.HIGH, 3),
        (Ticket.priority == TicketPriority.NORMAL, 2),
        (Ticket.priority == TicketPriority.LOW, 1),
    )

    queue = session.scalars(
        select(Ticket)
        .where(Ticket.responsible_id == None)
        .where(Ticket.status == TicketStatus.OPEN)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
        .order_by(priority_order.desc(), Ticket.created_at.asc())
    ).all()

    return {"tickets": queue}


def assign_responsible_technician(id: int, user: User, session: Session):
    check_require_role(user.role, UserRole.TECHNICIAN)
    ticket = get_ticket_by_id(id, session)
    ticket.responsible = user
    ticket.status = TicketStatus.IN_PROGRESS
    session.commit()
    session.refresh(ticket)

    return ticket


def remove_responsible_ticket_technician(id: int, user: User, session: Session):
    check_require_role(user.role, UserRole.TECHNICIAN)
    ticket = get_ticket_by_id(id, session, validation_assigned=False)

    if not ticket.responsible_id == user.id:
        raise TicketDoesNotBelongToUser()

    if ticket.status == TicketStatus.RESOLVED:
        raise InvalidTicketStatus()

    ticket.responsible = None
    ticket.status = TicketStatus.OPEN
    session.commit()
    session.refresh(ticket)

    return ticket


def my_queue(user: User, session: Session):
    tickets = session.scalars(
        select(Ticket)
        .where(Ticket.responsible_id == user.id)
        .where(Ticket.status == TicketStatus.IN_PROGRESS)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    ).all()

    return {"tickets": tickets}


def resolve_ticket_by_id(id: int, user: User, session: Session):
    ticket = session.scalar(
        select(Ticket).where(Ticket.id == id).where(Ticket.responsible == user)
    )
    if not ticket:
        raise TicketNotFound()

    ticket.status = TicketStatus.RESOLVED
    session.commit()
    session.refresh(ticket)

    return ticket
