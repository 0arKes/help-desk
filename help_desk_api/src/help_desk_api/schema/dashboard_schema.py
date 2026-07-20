from pydantic import BaseModel


class AdminDashboard(BaseModel):
    tickets_open: int
    tickets_in_progress: int
    tickets_resolved: int
    tickets_deleted: int

    tickets_created_today: int
    tickets_resolved_today: int

    employees: int
    technicians: int
    admins: int
