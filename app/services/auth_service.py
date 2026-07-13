from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.jwt_handler import create_access_token

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def signup(self, db: Session, user: UserCreate):

        existing_user = self.user_repository.get_by_email(db, user.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = User(
            full_name = user.full_name,
            email = user.email,
            password = hash_password(user.password),
        ) 

        return self.user_repository.create_user(db, new_user)
     
    def login(self, db: Session, email: str, password: str):

        existing_user = self.user_repository.get_by_email(db, email)

        if not existing_user:
            raise HTTPException(status_code=401, detail= "Invalid email or password")
        
        if not verify_password(password, existing_user.password):
            raise HTTPException(status_code=401, detail= "Invalid email or password")

        access_token = create_access_token({"sub": existing_user.email, "id": existing_user.id})

        return {
            "access_token": access_token,
            "token_type": "Bearer",
        }