import random
from app.repositories.otp_repository import OTPRepository
from sqlalchemy.orm import Session
from app.schemas.otp import SendOTPRequest, VerifyOTPRequest
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.otp import OTP
from app.utils.sms import SMSService
from app.core.logging import logger
from app.core.jwt_handler import create_access_token
from app.core.config import settings

class OTPService:
    def __init__(self):
        self.repository = OTPRepository()


    #generate otp
    def generate_otp(self):
        return str(
            random.randint(
                100000, 
                999999
            )
        )
    
    #send otp
    def send_otp(self, db: Session, request: SendOTPRequest):
        existing = self.repository.get_latest_otp(db, request.mobile)

        if existing:
            if (existing.expires_at > datetime.now() and not existing.is_used):
                raise HTTPException(
                    status_code=400,
                    detail= "OTP already sent. Please wait."
                )
            
        otp = self.generate_otp()
        expiry = datetime.utcnow() + timedelta(minutes= settings.OTP_EXPIRE_MINUTES)

        otp_record = OTP(
            mobile = request.mobile,
            otp = otp,
            expires_at = expiry
        )

        self.repository.create_otp(db, otp_record)

        SMSService.send_otp(request.mobile, otp)

        logger.info(f"OTP generated for {request.mobile}")

        return {
            "message" "OTP sent successfully"
        }
    

    #verify otp
    def verify_otp(self, db: Session, request: VerifyOTPRequest):
        otp_record = self.repository.get_latest_otp(db, request.mobile)

        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP not found")
        
        if otp_record.is_used:
            raise HTTPException(status_code=400, detail="OTP already used")
        
        if otp_record.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail= "OTP expired")
        
        if otp_record.attempt_count >= settings.OTP_MAX_ATTEMPTS:
            raise HTTPException(status_code=403, detail= "Maximum attempts exceeded")
        
        if otp_record.otp != request.otp:
            self.repository.increment_attempt(db, otp_record)
            raise HTTPException(status_code=400, detail="Inavalid OTP")
        
        self.repository.mark_as_used(db, otp_record)

        access_token = create_access_token({ "mobile": request.mobile})
        
        logger.info(f"OTP verified successfully for {request.mobile}")

        return {
            "access token": access_token,
            "token_type": "Bearer"
        }
        
    #Resend otp 
    def resend_otp(self, db: Session, request: SendOTPRequest):

        otp_record = self.repository.get_latest_otp(db,request.mobile)

        if otp_record:
            self.repository.delete_otp(db, otp_record)
            return self.send_otp(db, request)


    

