from fastapi import status
from httpx import Response


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "User test",
            "email": "user_email@test.com",
            "password": "123456",
            "role": "employee",
        },
    )
    response_json = response.json()

    assert response_json["id"] == 1
    assert response_json["name"] == "User test"
    assert response_json["email"] == "user_email@test.com"
    assert "password" not in response_json
    assert response_json["role"] == "employee"


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


def test_get_me(client, token):
    response = client.get("/auth/whoami", headers={"Authorization": f"Bearer {token}"})

    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["id"] == 1
    assert response_json["name"] == "test"
    assert response_json["email"] == "test@test.com"
    assert "password" not in response_json
    assert response_json["role"] == "admin"


def test_get_me_without_token(client):
    response: Response = client.get(
        "/auth/whoami", headers={"Authorization": "Bearer no_content"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
