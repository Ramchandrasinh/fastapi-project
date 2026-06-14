from app import schemas

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert res.status_code == 201
    new_user = schemas.UserOutput.model_validate(res.json())
    assert new_user.email == "user@example.com"

def test_login_user(client):
    client.post(
        "/users/",
        json={"email": "user@example.com", "password": "password123"},
    )
    res = client.post(
        "/auth/login/",
        data={"username": "user@example.com", "password": "password123"},
    )
    # print(res.json())
    assert res.status_code == 200
