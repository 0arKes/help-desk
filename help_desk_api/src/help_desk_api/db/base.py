from help_desk_api.config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import registry

mapper_registry = registry()
engine = create_engine(settings.database_url)
