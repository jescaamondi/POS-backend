def test_product_crud(client, category, supplier):
    payload = {
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "unit_price": "89.90",
        "stock_quantity": 25,
        "stock_unit": "pcs",
        "category_id": category["category_id"],
        "supplier_id": supplier["supplier_id"],
    }
    created = client.post("/products/", json=payload)
    assert created.status_code == 201, created.text
    product = created.json()
    product_id = product["product_id"]

    assert client.get(f"/products/{product_id}").status_code == 200
    assert len(client.get("/products/").json()) == 1

    updated = client.put(f"/products/{product_id}", json={"unit_price": "79.90", "stock_quantity": 30})
    assert updated.status_code == 200
    assert updated.json()["unit_price"] == "79.90"
    assert updated.json()["stock_quantity"] == 30

    assert client.delete(f"/products/{product_id}").status_code == 204
    assert client.get(f"/products/{product_id}").status_code == 404


def test_product_validation(client):
    response = client.post(
        "/products/",
        json={"name": "", "unit_price": "-1", "stock_quantity": -2, "stock_unit": "pcs"},
    )
    assert response.status_code == 422


def test_product_missing_resource(client):
    assert client.get("/products/no-such-product").status_code == 404
