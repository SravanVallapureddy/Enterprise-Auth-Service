from pydantic import BaseModel, Field

class SendOTPRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=10)

class VerifyOTPRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=10)
    otp: str = Field(min_length=6, max_length=6)

class OTPResponse(BaseModel):
    message: str

class OTPVerifyResponse(BaseModel):
    access_token: str
    token_type: str
