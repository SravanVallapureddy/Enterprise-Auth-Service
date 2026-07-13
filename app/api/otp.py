from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.otp import SendOTPRequest, VerifyOTPRequest 
from app.core.dependencies import get_db
from app.services.otp_service import OTPService

router = APIRouter(prefix="/otp", tags=["OTP Authentication"])

otp_service = OTPService()

@router.post("/send")
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    return otp_service.send_otp(db, request)

@router.post("/verify")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    return otp_service.verify_otp(db, request)

@router.post("/resend")
def resend_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    return otp_service.resend_otp(db, request)