from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_password
from repositories.user import UserRepository
from schemas.user import UserCreate

user_repository = UserRepository()


def register(db: Session, data: UserCreate):
    from services.user import create_user
    return create_user(db, data)


def authenticate(db: Session, username: str, password: str):
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token({"sub": user.username, "role": user.role}),
        "token_type": "bearer",
    }
