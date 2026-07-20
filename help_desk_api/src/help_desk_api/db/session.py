from help_desk_api.db.base import AsyncSessionLocal


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
