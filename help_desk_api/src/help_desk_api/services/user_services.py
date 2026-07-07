from fastapi.security import OAuth2PasswordRequestForm
from help_desk_api.db.models.user import User
from help_desk_api.exceptions import user_exceptions
from help_desk_api.schema.user_schema import CreateUser
from help_desk_api.security.password_hash import get_password_hash, verify_password_hash
from help_desk_api.security.token import create_access_token
from sqlalchemy import select
from sqlalchemy.orm import Session


# create user
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
        raise user_exceptions.EmailAlreadyExistsException()


# end of create user


def get_user_by_email(session: Session, email: str) -> User | None:
    get_user = session.scalar(select(User).where(User.email == email))

    return get_user


def get_user_by_id(session: Session, id: int) -> User | None:
    get_user = session.scalar(select(User).where(User.id == id))

    return get_user


def authenticate_user(session: Session, form: OAuth2PasswordRequestForm):
    user = get_user_by_email(session, form.username)

    if not user:
        raise user_exceptions.InvalidCredentials()
    if not verify_password_hash(form.password, user.password):
        raise user_exceptions.InvalidCredentials()

    token = create_access_token({"sub": str(user.id), "role": user.role.value})

    return {"access_token": token, "token_type": "Bearer"}
