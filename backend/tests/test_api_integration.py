from datetime import date


def test_journal_flow_register_login_create_calendar_delete(client):
    registered = client.post(
        "/auth/register",
        json={"email": "flow@example.com", "password": "Correct123!", "name": "Flow"},
    )
    assert registered.status_code == 201

    login = client.post(
        "/auth/login",
        json={"email": "flow@example.com", "password": "Correct123!"},
    )
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    created = client.post(
        "/calendar/logs",
        headers=headers,
        json={
            "drink_id": "iced-americano",
            "drink_name": "Iced Americano",
            "rating": 5,
        },
    )
    assert created.status_code == 201
    log_id = created.json()["id"]

    today = date.today()
    calendar = client.get(
        "/calendar/month",
        headers=headers,
        params={"year": today.year, "month": today.month},
    )
    assert calendar.status_code == 200
    entries = [
        entry
        for day in calendar.json()["days"]
        for entry in day["entries"]
    ]
    assert any(entry["id"] == log_id for entry in entries)
    assert any(entry["temperature_tag"] == "iced" for entry in entries)

    deleted = client.delete(f"/calendar/logs/{log_id}", headers=headers)
    assert deleted.status_code == 204

    after = client.get(
        "/calendar/month",
        headers=headers,
        params={"year": today.year, "month": today.month},
    )
    leftover = [
        entry
        for day in after.json()["days"]
        for entry in day["entries"]
    ]
    assert leftover == []


def test_personalized_recommendations_endpoint_uses_journal(client, auth_header):
    headers = auth_header(email="recs@example.com")
    client.post(
        "/calendar/logs",
        headers=headers,
        json={
            "drink_id": "iced-americano",
            "drink_name": "Iced Americano",
            "rating": 5,
        },
    )
    client.post(
        "/calendar/logs",
        headers=headers,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 4},
    )

    response = client.get("/recommendations/personalized", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["what_you_might_like"] is not None
    assert body["try_something_new"] is not None
    assert body["taste_profile"]["rated_count"] == 2
    assert body["what_you_might_like"]["drink_id"]
    assert body["try_something_new"]["explanation"]


def test_personalized_recommendations_empty_journal_hides_familiar(client, auth_header):
    headers = auth_header(email="empty@example.com")

    response = client.get("/recommendations/personalized", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["what_you_might_like"] is None
    assert body["try_something_new"] is not None


def test_personalized_recommendations_require_auth(client):
    response = client.get("/recommendations/personalized")

    assert response.status_code in (401, 403)
