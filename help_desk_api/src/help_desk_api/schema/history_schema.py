from datetime import datetime

from help_desk_api.db.enum.history_actions import HistoryAction
from pydantic import BaseModel, EmailStr


class ReadUserSimple(BaseModel):
    id: int
    email: EmailStr


class ReadTicketSimple(BaseModel):
    id: int
    title: str


class ReadTicketHistory(BaseModel):
    id: int
    ticket: ReadTicketSimple
    action: HistoryAction
    user: ReadUserSimple
    old_value: str
    new_value: str
    performed_at: datetime


class ReadHistories(BaseModel):
    histories: list[ReadTicketHistory]
