from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base
from models.weather import WeatherCondition



class WeatherForecastDaily(Base):
    __tablename__ = "weather_forecast_daily"

    weather_forecast_daily_id = Column(Integer, primary_key=True, index=True)
    weather_id = Column(Integer, ForeignKey("weather.weather_id"), nullable=False)
    forecast_date = Column(DateTime, nullable=False)
    forecast_temp_high = Column(Integer, nullable=False)
    forecast_temp_low = Column(Integer, nullable=False)
    forecast_condition = Column(Enum(WeatherCondition, name="weather_condition_enum"), nullable=False)

    weather = relationship("Weather", back_populates="daily_forecasts")

    def __repr__(self):
        return f"<WeatherForecastDaily(id={self.weather_forecast_daily_id}, weather_id={self.weather_id})>"
