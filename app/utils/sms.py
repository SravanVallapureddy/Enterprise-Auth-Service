from app.core.logging import logger

class SMSService:

    @staticmethod
    def send_otp(mobile: str, otp: str):
        logger.info(f"Sending OTP {otp} to mobile {mobile}")