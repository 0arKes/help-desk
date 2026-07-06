from fastapi import APIRouter, Depends, status
from help_desk_api.db.session import get_session
from help_desk_api.schema.user_schema import CreateUser, ReadUser
from help_desk_api.services.user_services import create_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ReadUser, status_code=status.HTTP_201_CREATED)
def create_registry(form: CreateUser, session: Session = Depends(get_session)):
    return create_user(session, form)
