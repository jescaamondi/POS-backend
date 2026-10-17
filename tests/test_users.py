def test_user_crud_and_password_is_not_exposed(client, user_payload):
    created = client.post("/users/", json=user_payload)
    assert created.status_code == 201, created.text
    user = created.json()
    user_id = user["user_id"]
    assert "password" not in user
    assert "password_hash" not in user

    assert client.get(f"/users/{user_id}").status_code == 200
    updated = client.put(f"/users/{user_id}", json={"role": "manager"})
    assert updated.status_code == 200
    assert updated.json()["role"] == "manager"

    assert client.delete(f"/users/{user_id}").status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404


def test_user_duplicate_username_and_email_are_rejected(client, user_payload):
    assert client.post("/users/", json=user_payload).status_code == 201
    duplicate_username = {**user_payload, "email": "other@example.com"}
    duplicate_email = {**user_payload, "username": "otheruser"}
    assert client.post("/users/", json=duplicate_username).status_code == 409
    assert client.post("/users/", json=duplicate_email).status_code == 409


def test_user_password_validation(client, user_payload):
    response = client.post("/users/", json={**user_payload, "password": "short"})
    assert response.status_code == 422
