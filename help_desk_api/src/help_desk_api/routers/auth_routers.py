from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from help_desk_api.db.session import get_session
from help_desk_api.schema.token_schema import AccessToken
from help_desk_api.schema.user_schema import CreateUser, ReadUser
from help_desk_api.security.auth_depedence import get_current_user
from help_desk_api.services.user_services import authenticate_user, create_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ReadUser, status_code=status.HTTP_201_CREATED)
def create_registry(form: CreateUser, session: Session = Depends(get_session)):
    return create_user(session, form)


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
def login(
    form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):

    return authenticate_user(session, form)


@router.get("/")
def test(user=Depends(get_current_user)):
    pass
