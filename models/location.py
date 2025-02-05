from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base

class Location(Base):
    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    teams = relationship("Team", back_populates="location")
    weather = relationship("Weather", back_populates="location")

    def __repr__(self):
        return f"<Location(location_id={self.location_id}, location_name={self.location_name})>"

