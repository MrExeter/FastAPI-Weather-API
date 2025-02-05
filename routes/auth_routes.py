import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.api_key import ApiKey
from models.user import User

router = APIRouter()

########################################################################################################################
# Generate API Key for a User
########################################################################################################################
@router.post("/generate-api-key", summary="Generate API Key for a User")
def generate_api_key(user_id: int, db: Session = Depends(get_db)):
    """Generates a new API key for a given user ID."""

    # Check if the user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user already has an active API key
    existing_key = db.query(ApiKey).filter(ApiKey.user_id == user_id).first()
    if existing_key:
        return {"message": "User already has an API key", "api_key": existing_key.api_key, "expires_at": existing_key.expires_at}

    # Generate a secure random API key
    api_key = secrets.token_urlsafe(32)  # Creates a secure 32-character key
    expires_at = datetime.now() + timedelta(days=30)  # API key valid for 30 days

    # Store the API key in the database
    new_api_key = ApiKey(user_id=user_id, api_key=api_key, expires_at=expires_at)
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)

    return {"api_key": api_key, "expires_at": expires_at}


