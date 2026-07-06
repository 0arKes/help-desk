from help_desk_api.db.models.user import User
from help_desk_api.exceptions import user_exceptions
from help_desk_api.schema.user_schema import CreateUser
from help_desk_api.security.password_hash import get_password_hash
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_user(session: Session, form: CreateUser) -> User:
    validate_email_available(session, form.email)

    new_user = User(
        name=form.name,
        email=form.email.lower(),
        password=get_password_hash(form.password),
        role=form.role,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def validate_email_available(session: Session, email: str):

    get_email = session.scalar(select(User).where(User.email == email))
    if get_email:
        raise user_exceptions.EmailAlreadyExistsException
