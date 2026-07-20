from fastapi import APIRouter, Depends, status
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.history_schema import ReadHistories
from help_desk_api.schema.user_schema import (
    CreateAdminUser,
    ReadUser,
)
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.ticket_history_services import get_ticket_histories
from help_desk_api.services.user_services import (
    create_admin_user,
)
from sqlalchemy.ext.asyncio import AsyncSession

router_admin = APIRouter(prefix="/admin", tags=["Admin"])


@router_admin.get(
    "/history", response_model=ReadHistories, status_code=status.HTTP_200_OK
)
async def get_history(
    authenticate_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await get_ticket_histories(authenticate_user, session)


@router_admin.post("/register/makeadmin", response_model=ReadUser)
async def create_admin(
    form: CreateAdminUser,
    authenticate_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await create_admin_user(form, authenticate_user, session)
