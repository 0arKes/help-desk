from datetime import UTC, datetime, time, timedelta

from help_desk_api.db.enum.ticket_status import TicketStatus
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tickets_open(session: AsyncSession) -> int:
    result = await session.scalars(
        select(Ticket).where(Ticket.status == TicketStatus.OPEN)
    )
    query = result.all()

    return len(query)


async def get_tickets_in_progress(session: AsyncSession) -> int:
    result = await session.scalars(
        select(Ticket).where(Ticket.responsible_id.is_not(None))
    )
    query = result.all()

    return len(query)


async def get_tickets_resolved(session: AsyncSession) -> int:
    result = await session.scalars(
        select(Ticket).where(Ticket.status == TicketStatus.RESOLVED)
    )
    query = result.all()

    return len(query)


async def get_tickets_deleted(session: AsyncSession) -> int:
    result = await session.scalars(
        select(Ticket).where(Ticket.status == TicketStatus.DELETED)
    )
    query = result.all()

    return len(query)


async def get_tickets_created_today(session: AsyncSession) -> int:
    today = datetime.now(UTC).date()
    start = datetime.combine(today, time.min, tzinfo=UTC)
    end = start + timedelta(days=1)

    result = await session.scalars(
        select(Ticket).where(Ticket.created_at >= start).where(Ticket.created_at < end)
    )
    query = result.all()

    return len(query)


async def get_tickets_resolved_today(session: AsyncSession) -> int:
    today = datetime.now(UTC).date()
    start = datetime.combine(today, time.min, tzinfo=UTC)
    end = start + timedelta(days=1)

    result = await session.scalars(
        select(Ticket)
        .where(Ticket.created_at >= start)
        .where(Ticket.created_at < end)
        .where(Ticket.status == TicketStatus.RESOLVED)
    )
    query = result.all()

    return len(query)


async def get_employees(session: AsyncSession) -> int:
    result = await session.scalars(select(User).where(User.role == UserRole.EMPLOYEE))
    query = result.all()

    return len(query)


async def get_technicians(session: AsyncSession) -> int:
    result = await session.scalars(select(User).where(User.role == UserRole.TECHNICIAN))
    query = result.all()

    return len(query)


async def get_admins(session: AsyncSession) -> int:
    result = await session.scalars(select(User).where(User.role == UserRole.ADMIN))
    query = result.all()

    return len(query)
