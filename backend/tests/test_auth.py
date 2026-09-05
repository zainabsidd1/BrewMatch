def test_registration_succeeds(client):
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "Correct123!"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert "id" in body
    assert "hashed_password" not in body


def test_duplicate_email_is_rejected(client, create_user):
    create_user(email="dup@example.com", password="Correct123!")

    response = client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "Correct123!"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_valid_login_succeeds(client, create_user):
    create_user(email="login@example.com", password="Correct123!")

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "Correct123!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_wrong_password_returns_401(client, create_user):
    create_user(email="test@example.com", password="Correct123!")

    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "Wrong123!"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_protected_route_rejects_missing_auth(client):
    response = client.get("/auth/me")

    assert response.status_code in (401, 403)


def test_protected_route_rejects_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401
