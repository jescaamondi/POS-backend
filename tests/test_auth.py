from datetime import datetime, timedelta, timezone

import jwt

from core.security import JWT_ALGORITHM, JWT_SECRET
from schemas.user import UserCreate
from services.user import create_user

PASSWORD = "StrongPass123"


def make_user(db_session, username="cashier1", role="cashier"):
    return create_user(
        db_session,
        UserCreate(
            first_name="Ann",
            last_name="Wanjiru",
            username=username,
            email=f"{username}@example.com",
            role=role,
            password=PASSWORD,
        ),
    )


def login(client, username="cashier1", password=PASSWORD):
    return client.post("/auth/login", json={"username": username, "password": password})


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_root_is_public(anon_client):
    assert anon_client.get("/").status_code == 200


def test_protected_endpoints_require_a_token(anon_client):
    for endpoint in ["/products/", "/sales/", "/users/", "/customer/"]:
        response = anon_client.get(endpoint)
        assert response.status_code == 401
        assert response.headers["WWW-Authenticate"] == "Bearer"

    response = anon_client.post("/categories/", json={"name": "Drinks"})
    assert response.status_code == 401


def test_login_returns_a_working_token(anon_client, db_session):
    make_user(db_session)

    response = login(anon_client)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"

    headers = auth_header(body["access_token"])
    me = anon_client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["username"] == "cashier1"
    assert "password" not in me.json()
    assert "password_hash" not in me.json()

    created = anon_client.post("/categories/", json={"name": "Drinks"}, headers=headers)
    assert created.status_code == 201


def test_login_rejects_wrong_password(anon_client, db_session):
    make_user(db_session)
    response = login(anon_client, password="WrongPass123")
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_rejects_unknown_user(anon_client):
    response = login(anon_client, username="nobody")
    assert response.status_code == 401


def test_inactive_user_cannot_log_in_or_use_old_token(anon_client, db_session):
    user = make_user(db_session)
    token = login(anon_client).json()["access_token"]

    user.is_active = False
    db_session.commit()

    assert login(anon_client).status_code == 401
    assert anon_client.get("/products/", headers=auth_header(token)).status_code == 401


def test_invalid_token_is_rejected(anon_client):
    response = anon_client.get("/products/", headers=auth_header("not-a-real-token"))
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_expired_token_is_rejected(anon_client, db_session):
    make_user(db_session)
    expired = jwt.encode(
        {"sub": "cashier1", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    response = anon_client.get("/products/", headers=auth_header(expired))
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"
