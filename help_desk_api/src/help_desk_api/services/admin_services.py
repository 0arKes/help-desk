from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.user import User
from help_desk_api.services.admin_core_services import (
    get_admins,
    get_employees,
    get_technicians,
    get_tickets_created_today,
    get_tickets_deleted,
    get_tickets_in_progress,
    get_tickets_open,
    get_tickets_resolved,
    get_tickets_resolved_today,
)
from help_desk_api.services.ticket_core_services import validate_require_role
from sqlalchemy.ext.asyncio import AsyncSession


async def dashboard(user: User, session: AsyncSession):
    validate_require_role(user.role, UserRole.ADMIN)

    response = {
        "tickets_open": await get_tickets_open(session),
        "tickets_in_progress": await get_tickets_in_progress(session),
        "tickets_resolved": await get_tickets_resolved(session),
        "tickets_deleted": await get_tickets_deleted(session),
        "tickets_created_today": await get_tickets_created_today(session),
        "tickets_resolved_today": await get_tickets_resolved_today(session),
        "employees": await get_employees(session),
        "technicians": await get_technicians(session),
        "admins": await get_admins(session),
    }

    return response
