import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from help_desk_api.db.base import mapper_registry
from help_desk_api.db.enum.user_role import UserRole
from help_desk_api.db.models.ticket import Ticket
from help_desk_api.db.models.user import User
from help_desk_api.db.session import get_session
from help_desk_api.main import app
from help_desk_api.security.password_hash import get_password_hash
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client(session):

    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    AsyncSessionMaker = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    async with AsyncSessionMaker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)

    await engine.dispose()


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


@pytest.fixture
def ticket(session, user) -> Ticket:
    new_ticket = Ticket(
        title="Title",
        description="Description",
        creator=user,
        responsible_id=None,
    )
    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)

    return new_ticket


@pytest.fixture
def user_employee(session) -> User:
    user = User(
        name="test employee",
        email="employee@test.com",
        password=get_password_hash("123456"),
        role=UserRole.EMPLOYEE,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token_employee(client, user_employee) -> str:
    response = client.post(
        "/auth/login", data={"username": user_employee.email, "password": "123456"}
    )
    response_token = response.json()
    return response_token.get("access_token")


@pytest.fixture
def user_technician(session) -> User:
    user = User(
        name="user technician",
        email="technician@test.com",
        password=get_password_hash("123456"),
        role=UserRole.TECHNICIAN,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token_technician(client, user_technician) -> str:
    response = client.post(
        "/auth/login", data={"username": user_technician.email, "password": "123456"}
    )
    response_token = response.json()
    return response_token.get("access_token")


@pytest.fixture
def user_secondary_technician(session) -> User:
    user = User(
        name="user secondary technician",
        email="technician2@test.com",
        password=get_password_hash("123456"),
        role=UserRole.TECHNICIAN,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token_secondary_technician(client, user_secondary_technician) -> str:
    response = client.post(
        "/auth/login",
        data={"username": user_secondary_technician.email, "password": "123456"},
    )
    response_token = response.json()
    return response_token.get("access_token")


@pytest.fixture
def assign_ticket(client, token_technician, ticket):
    response = client.post(
        "/ticket/technician/queue/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )
    return response


@pytest.fixture
def resolved_ticket(client, token_technician, ticket, assign_ticket):
    response = client.post(
        "/ticket/technician/queue/resolve/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )
    return response
