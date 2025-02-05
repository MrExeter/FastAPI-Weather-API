from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import enum

from database.base import Base


class WeatherCondition(str, enum.Enum):
    SUNNY = "Sunny"
    CLOUDY = "Cloudy"
    PARTLY_CLOUDY = "Partly Cloudy"
    OVERCAST = "Overcast"
    FOG = "Fog"
    RAIN = "Rain"
    SNOW = "Snow"



class Weather(Base):
    __tablename__ = "weather"

    weather_id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)
    temperature = Column(Integer, nullable=False)
    conditions = Column(Enum(WeatherCondition, name="weather_condition_enum"), nullable=False)
    last_updated = Column(DateTime, server_default=func.now())

    location = relationship("Location", back_populates="weather")
    hourly_forecasts = relationship("WeatherForecastHourly", back_populates="weather")
    daily_forecasts = relationship("WeatherForecastDaily", back_populates="weather")

    def __repr__(self):
        return f"<Weather(weather_id={self.weather_id}, location_id={self.location_id})>"
