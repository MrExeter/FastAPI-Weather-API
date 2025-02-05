import secrets
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database.database import get_db  # Database session
from models.api_key import ApiKey

# API Key Header in Requests
api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

def generate_api_key():
    return secrets.token_urlsafe(32)  # 32-character secure token

def create_api_key(user_id: int, db: Session):
    """Create and store a new API key for the user."""
    api_key = generate_api_key()
    expires_at = datetime.now() + timedelta(days=30)  # 30-day expiration

    db_api_key = ApiKey(user_id=user_id, api_key=api_key, expires_at=expires_at)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return {"api_key": api_key, "expires_at": expires_at}


def get_api_key(
    api_key: str = Security(api_key_header), db: Session = Depends(get_db)
):

    db_api_key = db.query(ApiKey).filter(ApiKey.api_key == api_key).first()

    if not db_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if db_api_key.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="API Key Expired")

    return db_api_key
