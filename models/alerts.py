from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Alerts(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String, unique=True, index=True, nullable=False)
    alert_description = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)

    team = relationship("Team", back_populates="alerts")

    def __repr__(self):
        return f"<Alerts(alert_id={self.alert_id}, alert_name={self.alert_name})>"
