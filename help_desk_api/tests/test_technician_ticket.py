from fastapi import status
from httpx import Response


### queue_all_tickets_without_responsible
def test_queue_without_responsible(client, ticket, token_technician):
    response: Response = client.get(
        "/ticket/technician/queue",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_get_queue_with_employee_token(client, ticket, token_employee):
    response: Response = client.get(
        "/ticket/technician/queue",
        headers={"Authorization": f"bearer {token_employee}"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


### assign_responsible_ticket
def test_assign_responsible_ticket(client, ticket, token_technician):
    response: Response = client.post(
        "/ticket/technician/queue/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["responsible"] == {"id": 2, "name": "user technician"}


def test_assign_already_assigned_ticket(
    client, assign_ticket, token_secondary_technician
):
    response: Response = client.post(
        "/ticket/technician/queue/1",
        headers={"Authorization": f"bearer {token_secondary_technician}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


### remove_responsible_ticket
def test_remove_responsible(client, assign_ticket, token_technician):
    response: Response = client.put(
        "/ticket/technician/queue/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["responsible"] is None


def test_remove_responsible_out_of_range(client, assign_ticket, token_technician):
    response: Response = client.put(
        "/ticket/technician/queue/99",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_remove_responsible_with_other_login(
    client, assign_ticket, token_secondary_technician
):
    response: Response = client.put(
        "/ticket/technician/queue/1",
        headers={"Authorization": f"bearer {token_secondary_technician}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


### get_my_queue
def test_get_queue(client, assign_ticket, token_technician):
    response: Response = client.get(
        "/ticket/technician/queue/me",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    assert response.status_code == status.HTTP_200_OK


### resolve_ticket
def test_resolve_ticket(client, assign_ticket, token_technician):
    response: Response = client.post(
        "/ticket/technician/queue/resolve/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_try_resolve_ticket_resolved(client, resolved_ticket, token_technician):
    response: Response = client.post(
        "/ticket/technician/queue/resolve/1",
        headers={"Authorization": f"bearer {token_technician}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
