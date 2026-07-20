from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket_history import TicketHistory
from help_desk_api.db.models.user import User
from help_desk_api.services.ticket_core_services import validate_require_role
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_ticket_histories(user: User, session: AsyncSession):
    validate_require_role(user.role, UserRole.ADMIN)
    results = await session.scalars(
        select(TicketHistory)
        .options(joinedload(TicketHistory.ticket), joinedload(TicketHistory.user))
        .order_by(TicketHistory.performed_at.desc())
    )
    history = results.all()

    return {"histories": history}
