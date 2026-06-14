from app import schemas


def create_user_and_token(client, email: str):
    client.post(
        "/users/",
        json={"email": email, "password": "password123"},
    )
    login_response = client.post(
        "/auth/login/",
        data={"username": email, "password": "password123"},
    )
    token = schemas.Token.model_validate(login_response.json())
    return token.access_token


def test_vote_add_and_remove(client):
    owner_token = create_user_and_token(client, "owner@example.com")
    voter_token = create_user_and_token(client, "voter@example.com")

    post_resp = client.post(
        "/posts/",
        json={"title": "Vote Post", "content": "Vote content"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    post = schemas.PostResponse.model_validate(post_resp.json())

    vote_resp = client.post(
        "/votes/",
        json={"post_id": post.id, "dir": 1},
        headers={"Authorization": f"Bearer {voter_token}"},
    )
    assert vote_resp.status_code == 201
    assert vote_resp.json()["message"] == "Vote added"

    remove_resp = client.post(
        "/votes/",
        json={"post_id": post.id, "dir": 0},
        headers={"Authorization": f"Bearer {voter_token}"},
    )
    assert remove_resp.status_code == 200
    assert remove_resp.json()["message"] == "Vote removed"


def test_vote_own_post_forbidden(client):
    owner_token = create_user_and_token(client, "selfvote@example.com")

    post_resp = client.post(
        "/posts/",
        json={"title": "My Post", "content": "Self vote"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    post = schemas.PostResponse.model_validate(post_resp.json())

    vote_resp = client.post(
        "/votes/",
        json={"post_id": post.id, "dir": 1},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert vote_resp.status_code == 403
    assert vote_resp.json()["detail"] == "Cannot vote on your own post"
