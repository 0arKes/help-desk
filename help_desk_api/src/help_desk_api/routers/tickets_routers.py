from fastapi import APIRouter, Depends, status
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.exceptions.ticket_exceptions import InvalidUserRole, TicketNotFound
from help_desk_api.schema.ticket_schema import CreateTicket, ReadMyTickets, ReadTicket
from help_desk_api.security.auth_depedence import get_current_user
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

router_ticket = APIRouter(prefix="/ticket", tags=["Ticket"])


@router_ticket.post("/", response_model=ReadTicket, status_code=status.HTTP_201_CREATED)
def create_ticket(
    form: CreateTicket,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if authenticate_user.role == UserRole.TECHNICIAN:
        raise InvalidUserRole()

    new_ticket = Ticket(
        title=form.title,
        description=form.description,
        creator=authenticate_user,
        priority=form.priority,
        responsible_id=None,
    )

    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket


@router_ticket.get("/", response_model=ReadMyTickets, status_code=status.HTTP_200_OK)
def read_my_tickets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    tickets = session.scalars(
        select(Ticket)
        .where(Ticket.creator_id == current_user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    ).all()
    return {"ticket": tickets}


@router_ticket.get("/{id}", response_model=ReadTicket, status_code=status.HTTP_200_OK)
def read_ticket_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    ticket = session.scalar(
        select(Ticket)
        .where(Ticket.id == id)
        .where(Ticket.creator_id == current_user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )
    if not ticket:
        raise TicketNotFound()
    return ticket
