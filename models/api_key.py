from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.base import Base

class ApiKey(Base):
    __tablename__ = "api_keys"

    api_key_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="api_keys")

    def __repr__(self):
        return f"<ApiKey(api_key_id={self.api_key_id}, user_id={self.user_id})>"

