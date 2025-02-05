from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.base import Base

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)
    wants_alerts = Column(Boolean, default=False)

    users = relationship("User", back_populates="team")
    location = relationship("Location", back_populates="teams")
    alerts = relationship("Alerts", back_populates="team")

    def __repr__(self):
        return f"<Team(team_id={self.team_id}, team_name={self.team_name}, wants_alerts={self.wants_alerts})>"

