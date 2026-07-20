from help_desk_api.config.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

mapper_registry = registry()
engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine)
