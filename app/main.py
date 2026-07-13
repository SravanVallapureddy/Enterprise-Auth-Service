from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.core.config import settings
from app.db.database import Base, engine

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.api.otp import router as otp_router 


Base.metadata.create_all(bind=engine)

app = FastAPI(title = settings.APP_NAME)

app.include_router(auth_router, tags=["Authentication"])
app.include_router(otp_router)
app.include_router(health_router, tags=["Health Check"])

@app.get("/")
def home():
    return {
        "message": settings.APP_NAME + " is running successfully"
    }