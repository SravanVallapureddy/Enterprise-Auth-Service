from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class OTP(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String(15), nullable=False)
    otp = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    attempt_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)