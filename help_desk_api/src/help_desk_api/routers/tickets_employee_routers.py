from fastapi import APIRouter, Depends, status
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.ticket_schema import (
    CreateTicket,
    ReadMyTickets,
    ReadTicket,
)
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.session_ticket_services import (
    create_ticket,
    delete_ticket,
    get_my_tickets,
    get_user_ticket_by_id,
    update_ticket,
)
from sqlalchemy.orm import Session

router_employee_ticket = APIRouter(prefix="/ticket", tags=["Ticket"])


@router_employee_ticket.post(
    "/", response_model=ReadTicket, status_code=status.HTTP_201_CREATED
)
def create_ticket_(
    form: CreateTicket,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):

    return create_ticket(form, authenticate_user, session)


@router_employee_ticket.get(
    "/", response_model=ReadMyTickets, status_code=status.HTTP_200_OK
)
def read_my_tickets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_my_tickets(current_user, session)


@router_employee_ticket.get(
    "/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK
)
def read_ticket_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_user_ticket_by_id(id, current_user, session)


@router_employee_ticket.put(
    "/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK
)
def update_ticket_without_responsible(
    id: int,
    form: CreateTicket,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return update_ticket(id, form, authenticate_user, session)


@router_employee_ticket.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_without_responsible(
    id: int,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return delete_ticket(id, authenticate_user, session)
