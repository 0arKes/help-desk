from fastapi import status
from httpx import Response


def test_create_ticket(client, token):
    response: Response = client.post(
        "/ticket/",
        headers={"Authorization": f"bearer {token}"},
        json={
            "title": "test-title",
            "description": "test-description",
            "priority": "low",
        },
    )

    response_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["id"] == 1
    assert response_json["title"] == "test-title"
    assert response_json["description"] == "test-description"
    assert response_json["creator"] == {
        "id": 1,
        "name": "test",
        "email": "test@test.com",
    }
    assert response_json["responsible"] is None
    assert response_json["status"] == "open"
    assert response_json["priority"] == "low"


def test_create_ticket_without_token(client):
    response: Response = client.post(
        "/ticket/",
        headers={"Authorization": "bearer test"},
        json={
            "title": "test-title",
            "description": "test-description",
            "priority": "low",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_technician_create_ticket(client, user_technician, token_technician):
    response: Response = client.post(
        "/ticket/",
        headers={"Authorization": f"bearer {token_technician}"},
        json={
            "title": "test-title",
            "description": "test-description",
            "priority": "low",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_ticket(client, ticket, token):
    response: Response = client.put(
        "/ticket/1",
        headers={"Authorization": f"bearer {token}"},
        json={
            "title": "update-title",
            "description": "update-description",
            "priority": "normal",
        },
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["id"] == 1
    assert response_json["title"] == "update-title"
    assert response_json["description"] == "update-description"
    assert response_json["creator"] == {
        "id": 1,
        "name": "test",
        "email": "test@test.com",
    }
    assert response_json["responsible"] is None
    assert response_json["status"] == "open"
    assert response_json["priority"] == "normal"


def test_update_ticket_out_of_rang(client, ticket, token):
    response: Response = client.put(
        "/ticket/99",
        headers={"Authorization": f"bearer {token}"},
        json={
            "title": "update-title",
            "description": "update-description",
            "priority": "normal",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_ticket_without_token(client, ticket):
    response: Response = client.put(
        "/ticket/1",
        headers={"Authorization": "bearer test"},
        json={
            "title": "update-title",
            "description": "update-description",
            "priority": "normal",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_ticket(client, ticket, token):
    response: Response = client.delete(
        "/ticket/1",
        headers={"Authorization": f"bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_my_tickets(client, ticket, token):
    response: Response = client.get(
        "/ticket/", headers={"Authorization": f"bearer {token}"}
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["tickets"][0]["id"] == 1
    assert response_json["tickets"][0]["title"] == "Title"
    assert response_json["tickets"][0]["description"] == "Description"
    assert response_json["tickets"][0]["creator"] == {
        "id": 1,
        "name": "test",
        "email": "test@test.com",
    }
    assert response_json["tickets"][0]["responsible"] is None
    assert response_json["tickets"][0]["status"] == "open"
    assert response_json["tickets"][0]["priority"] == "normal"


def test_read_ticket_by_id(client, ticket, token):
    response: Response = client.get(
        "/ticket/1", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
