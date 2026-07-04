from help_desk_api.db.base import engine
from sqlalchemy.orm import Session


def get_session():
    with Session(engine) as session:
        yield session
