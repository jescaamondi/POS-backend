def test_category_crud(client):
    created = client.post(
        "/categories/", json={"name": "Food", "description": "Food products"}
    )
    assert created.status_code == 201
    category = created.json()
    category_id = category["category_id"]

    assert client.get(f"/categories/{category_id}").status_code == 200
    listed = client.get("/categories/").json()
    assert any(item["category_id"] == category_id for item in listed)

    updated = client.put(f"/categories/{category_id}", json={"name": "Groceries"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Groceries"

    deleted = client.delete(f"/categories/{category_id}")
    assert deleted.status_code == 204
    assert client.get(f"/categories/{category_id}").status_code == 404


def test_category_missing_resource(client):
    response = client.get("/categories/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_category_validation(client):
    response = client.post("/categories/", json={"name": ""})
    assert response.status_code == 422
