from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.exceptions.ticket_exceptions import InvalidUserRole, TicketNotFound
from help_desk_api.schema.ticket_schema import CreateTicket
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


def check_require_role(user_role: UserRole, allowed_role: UserRole):
    if user_role == allowed_role or user_role == UserRole.ADMIN:
        return

    raise InvalidUserRole()


def create_ticket(form: CreateTicket, user: User, session: Session):

    check_require_role(user.role, UserRole.EMPLOYEE)

    new_ticket = Ticket(
        title=form.title,
        description=form.description,
        creator=user,
        priority=form.priority,
        responsible_id=None,
    )

    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket


def get_my_tickets(user: User, session: Session):

    tickets = session.scalars(
        select(Ticket)
        .where(Ticket.creator_id == user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    ).all()
    return {"ticket": tickets}


def get_tickets_by_id(id: int, user: User, session: Session):

    ticket = session.scalar(
        select(Ticket)
        .where(Ticket.id == id)
        .where(Ticket.creator_id == user.id)
        .options(joinedload(Ticket.creator), joinedload(Ticket.responsible))
    )
    if not ticket:
        raise TicketNotFound()
    return ticket
