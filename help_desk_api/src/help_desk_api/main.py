from fastapi import FastAPI

from help_desk_api.routers.auth_routers import router

app = FastAPI()

app.include_router(router)
