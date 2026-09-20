def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"My POS": "Welcome to the Point of Sale System API."}


def test_all_collection_endpoints_start_empty(client):
    endpoints = [
        "/users/", "/categories/", "/customer/", "/suppliers/", "/products/",
        "/sales/", "/sale-items/", "/payments/", "/receipts/",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, (endpoint, response.text)
        assert response.json() == []
