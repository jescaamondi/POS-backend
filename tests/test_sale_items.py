def test_sale_item_crud(client, sale, product):
    created = client.post(
        "/sale-items/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 2,
            "product_total": "20.00",
        },
    )
    assert created.status_code == 201, created.text
    item = created.json()
    item_id = item["sale_item_id"]

    assert client.get(f"/sale-items/{item_id}").status_code == 200
    updated = client.put(f"/sale-items/{item_id}", json={"quantity": 3})
    assert updated.status_code == 200
    assert updated.json()["quantity"] == 3
    assert client.delete(f"/sale-items/{item_id}").status_code == 204
    assert client.get(f"/sale-items/{item_id}").status_code == 404


def test_sale_item_validation(client, sale, product):
    response = client.post(
        "/sale-items/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 0,
            "product_total": "10",
        },
    )
    assert response.status_code == 422


def test_sale_item_requires_existing_references(client):
    response = client.post(
        "/sale-items/",
        json={
            "sale_id": "missing",
            "product_id": "missing",
            "quantity": 1,
            "product_total": "10",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Sale not found"
