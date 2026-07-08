import pytest
from fastapi.testclient import TestClient
from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.main import app
from help_desk_api.security.password_hash import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client(session):

    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    mapper_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def user(session) -> User:
    user = User(
        name="test",
        email="test@test.com",
        password=get_password_hash("123456"),
        role=UserRole.ADMIN,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user) -> str:
    response = client.post(
        "/auth/login", data={"username": user.email, "password": "123456"}
    )
    response_token = response.json()
    return response_token.get("access_token")
