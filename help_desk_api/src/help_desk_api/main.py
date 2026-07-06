from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.schema.user import CreateUser, ReadUser
from help_desk_api.security.password_hash import get_password_hash

app = FastAPI()


@app.post("/register", response_model=ReadUser, status_code=201)
def create_registry(form: CreateUser, session: Session = Depends(get_session)):
    new_user = User(
        name=form.name,
        email=form.email,
        password=get_password_hash(form.password),
        role=form.role,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
