from sqlalchemy.orm import Session
from app.models.otp import OTP

class OTPRepository:
    def create_otp(self, db: Session, otp_record: OTP):
        db.add(otp_record)
        db.commit()
        db.refresh(otp_record)
        return otp_record
    
    def get_latest_otp(self, db: Session, mobile: str):
        return (
            db.query(OTP)
            .filter(OTP.mobile == mobile)
            .order_by(OTP.created_at.desc())
            .first()
        )
    
    def mark_as_used(self, db: Session, otp_record: OTP):
        otp_record.is_used = True
        db.commit()
        db.refresh(otp_record)
        return otp_record
    
    def increment_attempt(self, db: Session, otp_record: OTP):
        otp_record.attempt_count += 1
        db.commit()
        db.refresh(otp_record)
        return otp_record
    
    def delete_otp(self, db: Session, otp_record: OTP):
        db.delete(otp_record)
        db.commit()