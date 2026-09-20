def test_receipt_crud(client, sale):
    created = client.post(
        "/receipts/", json={"sale_id": sale["sale_id"], "receipt_number": "R-001"}
    )
    assert created.status_code == 201, created.text
    receipt = created.json()
    receipt_id = receipt["receipt_id"]

    assert client.get(f"/receipts/{receipt_id}").status_code == 200
    updated = client.put(f"/receipts/{receipt_id}", json={"receipt_number": "R-002"})
    assert updated.status_code == 200
    assert updated.json()["receipt_number"] == "R-002"
    assert client.delete(f"/receipts/{receipt_id}").status_code == 204
    assert client.get(f"/receipts/{receipt_id}").status_code == 404


def test_receipt_validation(client, sale):
    response = client.post("/receipts/", json={"sale_id": sale["sale_id"], "receipt_number": ""})
    assert response.status_code == 422


def test_receipt_requires_existing_sale_and_is_unique_per_sale(client, sale):
    missing = client.post("/receipts/", json={"sale_id": "missing", "receipt_number": "R-404"})
    assert missing.status_code == 404

    payload = {"sale_id": sale["sale_id"], "receipt_number": "R-001"}
    assert client.post("/receipts/", json=payload).status_code == 201
    assert client.post("/receipts/", json=payload).status_code == 409
