from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from help_desk_api.config.settings import settings
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.exceptions.user_exceptions import InvalidTokenAccess
from help_desk_api.services.user_services import get_user_by_id
from jwt import InvalidTokenError, decode
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer("/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    try:
        payload = decode(token, settings.jwt_key, algorithms=[settings.jwt_algorithm])
    except InvalidTokenError:
        raise InvalidTokenAccess()

    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenAccess()

    user = get_user_by_id(session, int(user_id))
    if not user:
        raise InvalidTokenAccess

    return user
