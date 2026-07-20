from fastapi.security import OAuth2PasswordRequestForm
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.user import User
from help_desk_api.exceptions.user_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentials,
    NotAllowedAdmin,
)
from help_desk_api.schema.user_schema import CreateAdminUser, CreateUser, UpdateUser
from help_desk_api.security.password_hash import get_password_hash, verify_password_hash
from help_desk_api.security.token import create_access_token
from help_desk_api.services.ticket_core_services import validate_require_role
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, form: CreateUser) -> User:
    await validate_email_available(session, form.email)
    validate_admin_creation(form.role)

    new_user = User(
        name=form.name.capitalize(),
        email=form.email.lower(),
        password=get_password_hash(form.password),
        role=form.role,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def validate_email_available(session: AsyncSession, email: str):

    get_email = await get_user_by_email(session, email)

    if get_email:
        raise EmailAlreadyExistsException()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    get_user = await session.scalar(select(User).where(User.email == email))

    return get_user


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    get_user = await session.scalar(select(User).where(User.id == id))

    return get_user


async def authenticate_user(session: AsyncSession, form: OAuth2PasswordRequestForm):
    user = await get_user_by_email(session, form.username)

    if not user:
        raise InvalidCredentials()
    if not verify_password_hash(form.password, user.password):
        raise InvalidCredentials()

    token = create_access_token({"sub": str(user.id), "role": user.role.value})

    return {"access_token": token, "token_type": "Bearer"}


def validate_admin_creation(user_role: UserRole):
    if user_role == UserRole.ADMIN:
        raise NotAllowedAdmin()


async def update_current_user(form: UpdateUser, user: User, session: AsyncSession):

    if form.email != user.email:
        await validate_email_available(session, form.email)
        user.email = form.email.lower()

    user.password = get_password_hash(form.password)

    await session.commit()
    await session.refresh(user)
    return user


async def create_admin_user(form: CreateAdminUser, user: User, session: AsyncSession):
    validate_require_role(user.role, UserRole.ADMIN)
    await validate_email_available(session, form.email)

    new_user = User(
        name=form.name.capitalize(),
        email=form.email.lower(),
        password=get_password_hash(form.password),
        role=UserRole.ADMIN,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
