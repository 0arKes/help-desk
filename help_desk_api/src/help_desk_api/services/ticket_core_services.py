from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.exceptions.ticket_exceptions import (
    InvalidTicketResolvedStatus,
    InvalidTicketStatus,
    InvalidUserRole,
    TicketDoesNotBelongToUser,
    TicketHasBeenAssigned,
    TicketNotFound,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

### db


async def get_ticket_by_id(id: int, session: AsyncSession) -> Ticket:

    ticket = await session.scalar(
        select(Ticket)
        .where(Ticket.id == id)
        .where(Ticket.status != TicketStatus.DELETED)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )
    if not ticket:
        raise TicketNotFound()

    return ticket


async def get_open_employee_tickets(user: User, session: AsyncSession):
    results = await session.scalars(
        select(Ticket)
        .where(Ticket.creator_id == user.id)
        .where(Ticket.status == TicketStatus.OPEN)
        .where(Ticket.status != TicketStatus.DELETED)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )

    tickets = results.all()

    return {"tickets": tickets}


### logic


def validate_require_role(user_role: UserRole, allowed_role: UserRole):
    if user_role == allowed_role or user_role == UserRole.ADMIN:
        return

    raise InvalidUserRole()


def validate_ticket_not_assigned(ticket: Ticket):
    if ticket.responsible_id is not None:
        raise TicketHasBeenAssigned()
    return


def validate_ticket_user(ticket: Ticket, user: User):
    if ticket.creator_id != user.id:
        raise TicketDoesNotBelongToUser()


def validate_ticket_owner(ticket: Ticket, user: User):
    if ticket.responsible_id != user.id:
        raise TicketDoesNotBelongToUser()


def validate_ticket_not_resolved(ticket: Ticket):
    if ticket.status == TicketStatus.RESOLVED:
        raise InvalidTicketStatus()
    return


def validate_ticket_is_deleted(ticket: Ticket):
    if ticket.status == TicketStatus.DELETED:
        raise TicketNotFound()
    return


def validate_ticket_is_resolved(ticket: Ticket):
    if ticket.status != TicketStatus.RESOLVED:
        raise InvalidTicketResolvedStatus()
