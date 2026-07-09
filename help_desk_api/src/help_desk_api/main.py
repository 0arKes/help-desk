from fastapi import FastAPI

from help_desk_api.routers.auth_routers import router
from help_desk_api.routers.tickets_routers import router_ticket

app = FastAPI()

app.include_router(router)
app.include_router(router_ticket)
