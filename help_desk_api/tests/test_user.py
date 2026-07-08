from fastapi import status
from httpx import Response


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "User test",
            "email": "user_email@test.com",
            "password": "123456",
            "role": "admin",
        },
    )
    assert response.json()["id"] == 1
    assert response.json()["name"] == "User test"
    assert response.json()["email"] == "user_email@test.com"
    assert "password" not in response.json()
    assert response.json()["role"] == "admin"


def test_with_exist_email(client, user):
    response: Response = client.post(
        "/auth/register",
        json={
            "name": "User test",
            "email": "test@test.com",
            "password": "123456",
            "role": "admin",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_registry_password_short(client):
    response: Response = client.post(
        "/auth/register",
        json={
            "name": "User test",
            "email": "test@test.com",
            "password": "1",
            "role": "admin",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_access_token(client, user):
    response: Response = client.post(
        "/auth/login", data={"username": user.email, "password": "123456"}
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "Bearer"


def test_get_access_token_with_wrong_password(client, user):
    response: Response = client.post(
        "/auth/login", data={"username": user.email, "password": "xxxxxx"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_access_token_with_wrong_email(client):
    response: Response = client.post(
        "/auth/login", data={"username": "incorrect@email.com", "password": "123456"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
