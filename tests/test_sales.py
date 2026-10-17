def test_sale_crud(client, user, customer):
    created = client.post(
        "/sales/",
        json={
            "sale_amount": "100.00",
            "customer_id": customer["customer_id"],
            "user_id": user["user_id"],
        },
    )
    assert created.status_code == 201, created.text
    sale = created.json()
    sale_id = sale["sale_id"]

    assert client.get(f"/sales/{sale_id}").status_code == 200
    updated = client.put(f"/sales/{sale_id}", json={"sale_amount": "125.00"})
    assert updated.status_code == 200
    assert updated.json()["sale_amount"] == "125.00"
    assert client.delete(f"/sales/{sale_id}").status_code == 204
    assert client.get(f"/sales/{sale_id}").status_code == 404


def test_sale_validation(client, user):
    response = client.post(
        "/sales/", json={"sale_amount": -1, "user_id": user["user_id"]}
    )
    assert response.status_code == 422


def test_sale_missing_resource(client):
    assert client.get("/sales/no-such-sale").status_code == 404


def test_sale_requires_existing_user_and_customer(client):
    response = client.post(
        "/sales/",
        json={"sale_amount": "10", "user_id": "missing", "customer_id": "missing"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
