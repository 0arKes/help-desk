from datetime import datetime

from help_desk_api.db.enum.ticket_priority import TicketPriority
from help_desk_api.db.enum.ticket_status import TicketStatus
from pydantic import BaseModel, EmailStr, Field


class CreateTicket(BaseModel):
    title: str = Field(min_length=5, max_length=60)
    description: str
    priority: TicketPriority


class UserResponsible(BaseModel):
    id: int
    name: str


class UserCreator(BaseModel):
    id: int
    name: str
    email: EmailStr


class ReadTicket(BaseModel):
    id: int
    title: str
    description: str
    creator: UserCreator
    responsible: UserResponsible | None
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime


class ReadMyTickets(BaseModel):
    ticket: list[ReadTicket]
