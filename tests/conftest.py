import os

# Must be set before importing application modules so the test suite never uses
# the PostgreSQL development URL from app/.env.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET"] = "test-secret-for-pos-tests-32-bytes-long"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models  # noqa: F401 - registers all models
from core.dependencies import get_current_user
from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(test_engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: None
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def anon_client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def user_payload():
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "janedoe",
        "email": "jane@example.com",
        "role": "cashier",
        "password": "StrongPass123",
    }


@pytest.fixture()
def user(client, user_payload):
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def category(client):
    response = client.post(
        "/categories/", json={"name": "Electronics", "description": "Devices"}
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def supplier(client):
    response = client.post(
        "/suppliers/",
        json={
            "name": "Acme Supplies",
            "email_address": "sales@acme.example",
            "phone_number": "+31201234567",
            "address": "1 Main Street",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def customer(client):
    response = client.post(
        "/customer/",
        json={
            "first_name": "John",
            "last_name": "Smith",
            "phone_number": "+31207654321",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def product(client, category, supplier):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "14 inch laptop",
            "unit_price": "999.99",
            "stock_quantity": 10,
            "stock_unit": "pcs",
            "category_id": category["category_id"],
            "supplier_id": supplier["supplier_id"],
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def sale(client, user, customer):
    response = client.post(
        "/sales/",
        json={
            "sale_amount": "999.99",
            "customer_id": customer["customer_id"],
            "user_id": user["user_id"],
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def sale_item(client, sale, product):
    response = client.post(
        "/sale-items/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 1,
            "product_total": "999.99",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def payment(client, sale):
    response = client.post(
        "/payments/",
        json={"sale_id": sale["sale_id"], "payment_method": "card", "amount": "999.99"},
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def receipt(client, sale):
    response = client.post(
        "/receipts/",
        json={"sale_id": sale["sale_id"], "receipt_number": "R-10001"},
    )
    assert response.status_code == 201, response.text
    return response.json()
