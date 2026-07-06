from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.routers.auth_routers import router
from help_desk_api.schema.token_schema import AccessToken
from help_desk_api.security.password_hash import verify_password_hash
from help_desk_api.security.token import create_access_token

app = FastAPI()

app.include_router(router)


@app.post("/login", response_model=AccessToken)
def login(
    form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    get_user = session.scalar(select(User).where(User.email == form.username))
    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password_hash(form.password, get_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(get_user.id), "role": get_user.role.value})
    return {"access_token": token, "token_type": "Bearer"}
