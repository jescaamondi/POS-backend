def test_test_database_isolated_from_development_database(client):
    response = client.post("/categories/", json={"name": "Test Only"})
    assert response.status_code == 201
    assert client.get("/categories/").json()[0]["name"] == "Test Only"

    # The application dependency has been overridden with the in-memory SQLite
    # session. No PostgreSQL connection is used by this test.
    from database import DATABASE_URL
    assert DATABASE_URL.startswith("sqlite")
