def test_payment_crud(client, sale):
    created = client.post(
        "/payments/",
        json={"sale_id": sale["sale_id"], "payment_method": "cash", "amount": "50.00"},
    )
    assert created.status_code == 201, created.text
    payment = created.json()
    payment_id = payment["payment_id"]

    assert client.get(f"/payments/{payment_id}").status_code == 200
    updated = client.put(f"/payments/{payment_id}", json={"payment_method": "card"})
    assert updated.status_code == 200
    assert updated.json()["payment_method"] == "card"
    assert client.delete(f"/payments/{payment_id}").status_code == 204
    assert client.get(f"/payments/{payment_id}").status_code == 404


def test_payment_validation(client, sale):
    response = client.post(
        "/payments/",
        json={"sale_id": sale["sale_id"], "payment_method": "", "amount": -1},
    )
    assert response.status_code == 422


def test_payment_requires_existing_sale_and_is_unique_per_sale(client, sale):
    missing = client.post(
        "/payments/",
        json={"sale_id": "missing", "payment_method": "cash", "amount": "10"},
    )
    assert missing.status_code == 404

    payload = {"sale_id": sale["sale_id"], "payment_method": "cash", "amount": "10"}
    assert client.post("/payments/", json=payload).status_code == 201
    assert client.post("/payments/", json=payload).status_code == 409
