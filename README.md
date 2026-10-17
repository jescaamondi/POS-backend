# POS Backend

FastAPI backend for a Point of Sale system with PostgreSQL for development and an isolated SQLite database for automated tests.

## Run locally

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the PostgreSQL connection string and a secure `JWT_SECRET`.

Initialize the development database:

```bash
python -c "from database import init_db; init_db()"
```

Start the API:

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000` and its OpenAPI documentation is at `/docs`.

## Authentication

Every endpoint except `/` and `POST /auth/login` requires a JWT bearer token.

Create the first admin user:

```bash
python create_admin.py
```

Log in to get a token:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

Send the token on every other request:

```
Authorization: Bearer <access_token>
```

In `/docs`, click **Authorize** and paste the token to try the protected endpoints. `GET /auth/me` returns the logged-in user. Tokens expire after 30 minutes, and deactivated users are rejected even if their token has not expired yet.

## Run the tests

The test suite **does not use the PostgreSQL development database**. `tests/conftest.py` overrides the database dependency with an in-memory SQLite database and enables SQLite foreign-key enforcement.

Run the complete suite from the project root:

```bash
pytest
```

The suite covers the root endpoint, login and token protection, and CRUD, validation, missing-resource, duplicate-resource, relationship, and security scenarios across users, categories, customers, suppliers, products, sales, sale items, payments, and receipts.

## CI

GitHub Actions runs `pytest` on every push and on every pull request. The workflow is intentionally test-only; it does not deploy the application.
