import getpass

from database import SessionLocal, init_db
from schemas.user import UserCreate
from services.user import create_user


def main() -> None:
    init_db()
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password (min 8 characters): ")

    db = SessionLocal()
    try:
        user = create_user(
            db,
            UserCreate(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                role="admin",
                password=password,
            ),
        )
        print(f"Admin user '{user.username}' created.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
