def test_customer_crud(client):
    created = client.post("/customer/", json={"first_name": "Alice", "last_name": "Jones"})
    assert created.status_code == 201
    customer = created.json()
    customer_id = customer["customer_id"]
    assert customer["loyalty_points"] == 0

    assert client.get(f"/customer/{customer_id}").status_code == 200
    updated = client.put(f"/customer/{customer_id}", json={"loyalty_points": 20})
    assert updated.status_code == 200
    assert updated.json()["loyalty_points"] == 20

    assert client.delete(f"/customer/{customer_id}").status_code == 204
    assert client.get(f"/customer/{customer_id}").status_code == 404


def test_customer_validation(client):
    response = client.post("/customer/", json={"first_name": "", "last_name": "Jones", "loyalty_points": -1})
    assert response.status_code == 422
