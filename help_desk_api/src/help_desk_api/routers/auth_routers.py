from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.token_schema import AccessToken
from help_desk_api.schema.user_schema import (
    CreateUser,
    ReadUser,
    UpdateUser,
)
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.user_services import (
    authenticate_user,
    create_user,
    update_current_user,
)
from sqlalchemy.orm import Session

router_user = APIRouter(prefix="/auth", tags=["Authentication"])


@router_user.post(
    "/register", response_model=ReadUser, status_code=status.HTTP_201_CREATED
)
def create_registry(form: CreateUser, session: Session = Depends(get_session)):
    return create_user(session, form)


@router_user.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
def login(
    form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):

    return authenticate_user(session, form)


@router_user.get("/whoami", response_model=ReadUser, status_code=status.HTTP_200_OK)
def test(user: User = Depends(get_current_user)):
    return user


@router_user.put("/", response_model=ReadUser)
def update_registry(
    form: UpdateUser,
    authenticate_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return update_current_user(form, authenticate_user, session)
