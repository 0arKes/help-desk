from fastapi import APIRouter, Depends, status
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.history_schema import ReadHistories
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.ticket_history_services import get_ticket_histories
from sqlalchemy.orm import Session

router_admin = APIRouter(prefix="/admin", tags=["Admin"])


@router_admin.get(
    "/history", response_model=ReadHistories, status_code=status.HTTP_200_OK
)
def get_history(
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_ticket_histories(authenticate_user, session)
