from app import schemas


def create_user_and_token(client, email: str = "post@example.com"):
    response = client.post(
        "/users/",
        json={"email": email, "password": "password123"},
    )
    user = schemas.UserOutput.model_validate(response.json())
    login_response = client.post(
        "/auth/login/",
        data={"username": email, "password": "password123"},
    )
    token = schemas.Token.model_validate(login_response.json())
    return token.access_token


def test_create_and_read_post(client):
    token = create_user_and_token(client)
    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Hello world"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    post = schemas.PostResponse.model_validate(response.json())
    assert post.title == "Test Post"
    assert post.owner.email == "post@example.com"

    get_resp = client.get(f"/posts/{post.id}")
    assert get_resp.status_code == 200
    fetched = schemas.PostResponse.model_validate(get_resp.json())
    assert fetched.id == post.id
    assert fetched.votes == 0


def test_update_post_not_authorized(client):
    token = create_user_and_token(client, "owner@example.com")
    post_resp = client.post(
        "/posts/",
        json={"title": "Update Test", "content": "Initial"},
        headers={"Authorization": f"Bearer {token}"},
    )
    post = schemas.PostResponse.model_validate(post_resp.json())

    other_token = create_user_and_token(client, "other@example.com")

    response = client.put(
        f"/posts/{post.id}",
        json={"title": "Hacked", "content": "Nope"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403
