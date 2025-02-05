from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=True)

    team = relationship("Team", back_populates="users")
    api_keys = relationship("ApiKey", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email})>"
