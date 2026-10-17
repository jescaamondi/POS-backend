from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models.user import UserModel
from schemas.auth import LoginRequest, Token
from schemas.user import UserRead
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.authenticate(db, data.username, data.password)


@router.get("/me", response_model=UserRead)
def me(current_user: UserModel = Depends(get_current_user)):
    return current_user
