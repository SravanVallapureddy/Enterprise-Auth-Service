from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "message": "Enterprise Auth Service Running Successfully",
    }