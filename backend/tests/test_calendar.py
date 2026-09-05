from datetime import date


def test_create_journal_entry(client, auth_header):
    headers = auth_header()

    response = client.post(
        "/calendar/logs",
        headers=headers,
        json={
            "drink_id": "latte",
            "drink_name": "Caramel Latte",
            "rating": 4,
            "temperature": "hot",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["drink_id"] == "latte"
    assert body["drink_name"] == "Caramel Latte"
    assert body["rating"] == 4
    assert body["temperature_tag"] == "hot"
    assert body["date_tried"] == date.today().isoformat()


def test_retrieve_journal_entries(client, auth_header):
    headers = auth_header()
    client.post(
        "/calendar/logs",
        headers=headers,
        json={"drink_id": "mocha", "drink_name": "Mocha", "rating": 5, "temperature": "iced"},
    )

    listed = client.get("/calendar/logs", headers=headers)
    assert listed.status_code == 200
    entries = listed.json()
    assert len(entries) == 1
    assert entries[0]["drink_name"] == "Mocha"
    assert entries[0]["temperature_tag"] == "iced"

    today = date.today()
    month = client.get(
        "/calendar/month",
        headers=headers,
        params={"year": today.year, "month": today.month},
    )
    assert month.status_code == 200
    days = month.json()["days"]
    assert any(
        entry["drink_name"] == "Mocha"
        for day in days
        for entry in day["entries"]
    )


def test_delete_journal_entry(client, auth_header):
    headers = auth_header()
    created = client.post(
        "/calendar/logs",
        headers=headers,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 3},
    )
    log_id = created.json()["id"]

    deleted = client.delete(f"/calendar/logs/{log_id}", headers=headers)
    assert deleted.status_code == 204

    listed = client.get("/calendar/logs", headers=headers)
    assert listed.json() == []


def test_invalid_rating_is_rejected(client, auth_header):
    headers = auth_header()

    too_high = client.post(
        "/calendar/logs",
        headers=headers,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 6},
    )
    too_low = client.post(
        "/calendar/logs",
        headers=headers,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 0},
    )

    assert too_high.status_code == 422
    assert too_low.status_code == 422


def test_user_cannot_delete_another_users_entry(client, auth_header):
    owner = auth_header(email="owner@example.com")
    created = client.post(
        "/calendar/logs",
        headers=owner,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 5},
    )
    log_id = created.json()["id"]

    other = auth_header(email="other@example.com")
    response = client.delete(f"/calendar/logs/{log_id}", headers=other)

    assert response.status_code == 404
    remaining = client.get("/calendar/logs", headers=owner)
    assert len(remaining.json()) == 1


def test_user_cannot_edit_another_users_entry(client, auth_header):
    owner = auth_header(email="owner2@example.com")
    created = client.post(
        "/calendar/logs",
        headers=owner,
        json={"drink_id": "latte", "drink_name": "Latte", "rating": 2},
    )
    log_id = created.json()["id"]

    other = auth_header(email="other2@example.com")
    response = client.patch(
        f"/calendar/logs/{log_id}",
        headers=other,
        json={"rating": 5},
    )

    assert response.status_code == 404
    original = client.get("/calendar/logs", headers=owner)
    assert original.json()[0]["rating"] == 2
