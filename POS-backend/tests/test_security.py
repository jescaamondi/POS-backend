from core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hashing():
    password = "testpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_access_token_round_trip():
    token = create_access_token({"sub": "user-123", "role": "cashier"})
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "cashier"
