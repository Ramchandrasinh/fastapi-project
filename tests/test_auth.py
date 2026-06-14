from app import schemas
import pytest


def test_create_user_and_login(client):
    response = client.post(
        "/users/",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    created_user = schemas.UserOutput.model_validate(response.json())
    assert created_user.email == "login@example.com"
    assert created_user.id is not None

    login_response = client.post(
        "/auth/login/",
        data={"username": "login@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    token_data = schemas.Token.model_validate(login_response.json())
    assert token_data.access_token
    assert token_data.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@example.com", "password123", 403),
    ("login@example.com", "wrongpass", 403),
    ("wrong@example.com", "wrongpass", 403),
])
def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login/",
        data={"username": email, "password": password},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid email or password"
