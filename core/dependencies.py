import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.security import decode_access_token
from database import get_db
from models.user import UserModel
from repositories.user import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)
user_repository = UserRepository()


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    if credentials is None:
        raise _unauthorized("Not authenticated")
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise _unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise _unauthorized("Invalid token")
    username = payload.get("sub")
    user = user_repository.get_by_username(db, username) if username else None
    if not user or not user.is_active:
        raise _unauthorized("Invalid token")
    return user
