from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.alerts import Alerts
from models.weather import Weather
from models.weather_forecast_daily import WeatherForecastDaily
from models.weather_forecast_hourly import WeatherForecastHourly
from security.security import get_api_key

# Create Router
router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not Found"}},
)

########################################################################################################################
# get the current weather for a location
########################################################################################################################
@router.get("/{location_id}", summary="Get Current Weather")
def get_weather(location_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    weather = db.query(Weather).filter(Weather.location_id == location_id).first()

    if not weather:
        return {"message": "No weather data available for this location"}

    return {
        "location_id": weather.location_id,
        "temperature": weather.temperature,
        "condition": weather.conditions,
        "last_updated": weather.last_updated,
    }

########################################################################################################################
# get the hourly weather forecast for a location e.g. the next 12-24 hours
########################################################################################################################
@router.get("/{location_id}/hourly", summary="Get Hourly Weather Forecast")
def get_hourly_forecast(location_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    hourly_forecast = db.query(WeatherForecastHourly).filter(WeatherForecastHourly.weather_id == location_id).all()

    if not hourly_forecast:
        return {"message": "No hourly forecast available"}

    return [
        {
            "forecast_time": hour.forecast_time,
            "forecast_temp": hour.forecast_temp,
            "forecast_condition": hour.forecast_condition,
        }
        for hour in hourly_forecast
    ]

########################################################################################################################
# get the daily weather forecast for a location e.g. the next 10 days or whatever is available, could be an option?
########################################################################################################################
@router.get("/{location_id}/daily", summary="Get Daily Weather Forecast")
def get_daily_forecast(location_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    daily_forecast = db.query(WeatherForecastDaily).filter(WeatherForecastDaily.weather_id == location_id).all()

    if not daily_forecast:
        return {"message": "No daily forecast available"}

    return [
        {
            "forecast_date": day.forecast_date,
            "high_temp": day.forecast_temp_high,
            "low_temp": day.forecast_temp_low,
            "forecast_condition": day.forecast_condition,
        }
        for day in daily_forecast
    ]
