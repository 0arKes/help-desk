from datetime import UTC, datetime, timedelta

from help_desk_api.config.settings import settings
from jwt import encode


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_timedelta = datetime.now(tz=UTC) + timedelta(minutes=settings.jwt_exp)
    to_encode.update({"exp": expire_timedelta})
    return encode(to_encode, key=settings.jwt_key, algorithm=settings.jwt_algorithm)
