from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken

class TokenRepository:

    def create_token(self, db: Session, token: RefreshToken):
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def get_token(self, db: Session, token: str):
        return(
            db.query(RefreshToken).filter(RefreshToken.token == token).first()
        )
    
    def delete_token(self, db: Session, token: str):
        db_token = self.get_token(db, token)

        if db_token:
            db.delete(db_token)
            db.commit()
            return db_token
    
    def delete_user_tokens(self, db: Session, user_id: int):
        db_tokens = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
        for token in db_tokens:
            db.delete(token)
            db.commit()
            return True