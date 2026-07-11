from fastapi import FastAPI

from help_desk_api.routers.auth_routers import router
from help_desk_api.routers.tickets_employee_routers import router_employee_ticket
from help_desk_api.routers.tickets_technician_routers import router_technician_ticket

app = FastAPI()

app.include_router(router)
app.include_router(router_employee_ticket)
app.include_router(router_technician_ticket)
