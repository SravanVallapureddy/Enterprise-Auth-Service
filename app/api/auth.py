from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService()
    return auth_service.signup(db, user)

@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService()
    return auth_service.login(db, login_request.email, login_request.password)