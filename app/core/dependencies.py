from app.db.database import sessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.core.jwt_handler import decode_access_token
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = decode_access_token(token)
 
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid_token")
    
    return payload
