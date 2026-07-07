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
    assert response.json() == {
        "id": 1,
        "name": "User test",
        "email": "user_email@test.com",
        "role": "admin",
    }


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

    assert response.status_code == 409
