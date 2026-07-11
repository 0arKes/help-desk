from fastapi import APIRouter, Depends
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.ticket_schema import ReadTicketsWithoutResponsible
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.session_ticket_services import queue_without_responsible
from sqlalchemy.orm import Session

router_technician_ticket = APIRouter(
    prefix="/ticket/technician", tags=["Ticket for Technician Users"]
)


@router_technician_ticket.get("/queue", response_model=ReadTicketsWithoutResponsible)
def queue_all_tickets_without_responsible(
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return queue_without_responsible(authenticate_user, session)
