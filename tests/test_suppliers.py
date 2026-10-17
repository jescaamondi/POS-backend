def test_supplier_crud(client):
    payload = {
        "name": "Supplier One",
        "email_address": "supplier@example.com",
        "phone_number": "123456789",
        "address": "Market Road",
    }
    created = client.post("/suppliers/", json=payload)
    assert created.status_code == 201
    supplier = created.json()
    supplier_id = supplier["supplier_id"]

    assert client.get(f"/suppliers/{supplier_id}").status_code == 200
    updated = client.put(f"/suppliers/{supplier_id}", json={"name": "Supplier Updated"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Supplier Updated"
    assert client.delete(f"/suppliers/{supplier_id}").status_code == 204
    assert client.get(f"/suppliers/{supplier_id}").status_code == 404


def test_supplier_invalid_email(client):
    response = client.post(
        "/suppliers/",
        json={
            "name": "Supplier",
            "email_address": "not-an-email",
            "phone_number": "1",
            "address": "A",
        },
    )
    assert response.status_code == 422
