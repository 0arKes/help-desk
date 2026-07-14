from fastapi import APIRouter, Depends, status
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.ticket_schema import (
    ReadMyTickets,
    ReadTicket,
    ReadTicketsWithoutResponsible,
)
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.ticket_technician_services import (
    assign_responsible_technician,
    my_queue,
    queue_without_responsible,
    remove_responsible_ticket_technician,
    resolve_ticket_by_id,
)
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


@router_technician_ticket.post(
    "/queue/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK
)
def assign_responsible_ticket(
    id: int,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return assign_responsible_technician(id, authenticate_user, session)


@router_technician_ticket.put(
    "/queue/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK
)
def remove_responsible_ticket(
    id: int,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return remove_responsible_ticket_technician(id, authenticate_user, session)


@router_technician_ticket.get(
    "/queue/me", response_model=ReadMyTickets, status_code=status.HTTP_200_OK
)
def get_my_queue(
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return my_queue(authenticate_user, session)


@router_technician_ticket.post(
    "/queue/resolve/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK
)
def resolve_ticket(
    id: int,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return resolve_ticket_by_id(id, authenticate_user, session)
