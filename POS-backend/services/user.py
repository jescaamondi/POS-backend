from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password

user_repository = UserRepository()


def get_user(db: Session, user_id: str):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def list_users(db: Session):
    return user_repository.get_all(db)


def create_user(db: Session, data: UserCreate):
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    if user_repository.get_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    values = data.model_dump(exclude={"password"})
    values["password_hash"] = hash_password(data.password)
    return user_repository.create(db, values)


def update_user(db: Session, user_id: str, data: UserUpdate):
    db_user = get_user(db, user_id)
    values = data.model_dump(exclude_unset=True, exclude={"password"})
    if data.username and data.username != db_user.username and user_repository.get_by_username(db, data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    if data.email and data.email != db_user.email and user_repository.get_by_email(db, data.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    if data.password:
        values["password_hash"] = hash_password(data.password)
    return user_repository.update(db, db_user, values)


def delete_user(db: Session, user_id: str):
    return user_repository.remove(db, get_user(db, user_id))
