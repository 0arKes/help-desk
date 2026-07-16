from help_desk_api.db.enum.history_actions import HistoryAction
from help_desk_api.db.enum.ticket_priority import TicketPriority
from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.services.history import create_ticket_history
from help_desk_api.services.ticket_core_services import (
    get_ticket_by_id,
    validate_require_role,
    validate_ticket_not_assigned,
    validate_ticket_not_resolved,
    validate_ticket_owner,
)
from sqlalchemy import case, select
from sqlalchemy.orm import Session, joinedload


def queue_without_responsible(user: User, session: Session):
    validate_require_role(user.role, UserRole.TECHNICIAN)

    priority_order = case(
        (Ticket.priority == TicketPriority.HIGH, 3),
        (Ticket.priority == TicketPriority.NORMAL, 2),
        (Ticket.priority == TicketPriority.LOW, 1),
    )

    queue = session.scalars(
        select(Ticket)
        .where(Ticket.responsible_id.is_(None))
        .where(Ticket.status == TicketStatus.OPEN)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
        .order_by(priority_order.desc(), Ticket.created_at.asc())
    ).all()

    return {"tickets": queue}


def assign_responsible_technician(id: int, user: User, session: Session):
    validate_require_role(user.role, UserRole.TECHNICIAN)
    ticket = get_ticket_by_id(id, session)
    validate_ticket_not_assigned(ticket)
    validate_ticket_not_resolved(ticket)

    history = create_ticket_history(
        ticket,
        HistoryAction.ASSIGNED,
        user,
        TicketStatus.OPEN.value,
        TicketStatus.IN_PROGRESS.value,
    )
    ticket.responsible = user
    ticket.status = TicketStatus.IN_PROGRESS

    session.add(history)
    session.commit()
    session.refresh(ticket)

    return ticket


def remove_responsible_ticket_technician(id: int, user: User, session: Session):
    validate_require_role(user.role, UserRole.TECHNICIAN)
    ticket = get_ticket_by_id(id, session)
    validate_ticket_owner(ticket, user)
    validate_ticket_not_resolved(ticket)

    history = create_ticket_history(
        ticket,
        HistoryAction.UNASSIGNED,
        user,
        _old_value=TicketStatus.IN_PROGRESS.value,
        _new_value=TicketStatus.OPEN.value,
    )

    ticket.responsible = None
    ticket.status = TicketStatus.OPEN

    session.add(history)
    session.commit()
    session.refresh(ticket)

    return ticket


def my_queue(user: User, session: Session):
    validate_require_role(user.role, UserRole.TECHNICIAN)
    tickets = session.scalars(
        select(Ticket)
        .where(Ticket.responsible_id == user.id)
        .where(Ticket.status == TicketStatus.IN_PROGRESS)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    ).all()

    return {"tickets": tickets}


def resolve_ticket_by_id(id: int, user: User, session: Session):
    validate_require_role(user.role, UserRole.TECHNICIAN)
    ticket = get_ticket_by_id(id, session)
    validate_ticket_owner(ticket, user)
    validate_ticket_not_resolved(ticket)

    history = create_ticket_history(
        ticket,
        HistoryAction.RESOLVED,
        user,
        _old_value=TicketStatus.IN_PROGRESS.value,
        _new_value=TicketStatus.RESOLVED.value,
    )

    ticket.status = TicketStatus.RESOLVED

    session.add(history)
    session.commit()
    session.refresh(ticket)

    return ticket
