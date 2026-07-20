import pytest
from fastapi.testclient import TestClient

from app.jso import app
from app.services.user_service import reset_users


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_fake_db():
    reset_users()
    yield
    reset_users()


def user_payload(**changes):
    payload = {
        "username": "jangsangok",
        "email": "sangok@example.com",
        "password": "1234",
        "bio": "FastAPI를 공부하고 있습니다.",
    }
    payload.update(changes)
    return payload


def create_user(**changes):
    return client.post("/users", json=user_payload(**changes))


def test_create_user():
    response = create_user()
    assert response.status_code == 201
    assert response.json() == {
        "user_id": 1,
        "username": "jangsangok",
        "email": "sangok@example.com",
        "bio": "FastAPI를 공부하고 있습니다.",
    }
    assert "password" not in response.json()


def test_get_all_users():
    create_user()
    create_user(username="second", email="second@example.com")
    response = client.get("/users")
    assert response.status_code == 200
    assert [user["user_id"] for user in response.json()] == [1, 2]
    assert all("password" not in user for user in response.json())


def test_get_user():
    create_user()
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "jangsangok"
    assert "password" not in response.json()


def test_update_user():
    create_user()
    response = client.put(
        "/users/1",
        json=user_payload(username="updated", email="updated@example.com", bio=None),
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "username": "updated",
        "email": "updated@example.com",
        "bio": None,
    }
    assert "password" not in response.json()


def test_delete_user():
    create_user()
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    assert "password" not in response.json()
    assert client.get("/users/1").status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_user_returns_404(method):
    request = getattr(client, method)
    kwargs = {"json": user_payload()} if method == "put" else {}
    response = request("/users/999", **kwargs)
    assert response.status_code == 404


@pytest.mark.parametrize("missing_field", ["username", "email", "password"])
def test_create_user_requires_mandatory_fields(missing_field):
    payload = user_payload()
    payload.pop(missing_field)
    response = client.post("/users", json=payload)
    assert response.status_code == 422
