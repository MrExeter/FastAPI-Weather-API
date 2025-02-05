import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the parent directory to sys.path, KLUGE!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.weather import Weather, WeatherCondition
from models.weather_forecast_hourly import WeatherForecastHourly
from models.weather_forecast_daily import WeatherForecastDaily
from models.location import Location
from models.team import Team
from models.user import User
from database.base import Base

from database.database import SessionLocal, engine


########################################################################################################################
# Generate Mock Teams
########################################################################################################################
def generate_mock_teams(db: Session):
    """Generates mock teams."""
    team_names = ["Paper Shufflers",
                  "Stapler Squad",
                  "Gossip Trackers",
                  "Lunch Crew",
                  "Extreme Weather Crew",
                  "Sunny Day Squad",
                  "Rainy Day Crew",
                  "Snow Patrol",
                  "Heatwave Heroes",
                  "Frostbite Fighters",
                  "Bare Knuckle Brawlers",
                  "Storm Chasers",
                  "Weather Wizards",]

    locations = db.query(Location).all()  # ✅ Get existing locations

    if not locations:
        print("No locations found. Cannot create teams.")
        return

    for name in team_names:
        location = random.choice(locations)
        team = Team(
            team_name=name,
            description=f"Team monitoring weather: {name}",
            location_id=location.location_id,
            wants_alerts=random.choice([True, False])  # ✅ Randomly assigns alert preference
        )
        db.add(team)

    db.commit()
    print("Mock teams generated!")

########################################################################################################################
# Generate Mock Users
########################################################################################################################
def generate_mock_users(db: Session):
    """Generates mock users and assigns them to teams."""
    teams = db.query(Team).all()

    if not teams:
        print("No teams found. Cannot create users.")
        return

    for i in range(100):  # Generate 100 users
        team = random.choice(teams)
        user = User(
            email=f"user{i+1}@weatherapi.com",
            password_hash="hashedpassword123",
            team_id=team.team_id
        )
        db.add(user)

    db.commit()
    print("✅ Mock users generated and assigned to teams!")


########################################################################################################################
# Generate Mock Locations
########################################################################################################################
def generate_mock_locations(db: Session):
    location_names = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "San Francisco", "Miami", "Seattle", "Denver", "Boston"
    ]

    for name in location_names:
        existing_location = db.query(Location).filter(Location.location_name == name).first()
        if not existing_location:
            location = Location(location_name=name, description=f"Weather data for {name}")
            db.add(location)

    db.commit()
    print("locations generated!")



########################################################################################################################
# Generate Random Weather Data
########################################################################################################################
def generate_weather_data(db: Session):
    """Generates mock weather data for locations."""
    locations = db.query(Location).all()

    if not locations:
        print("No locations found in the database.")
        return

    for location in locations:
        # Generate current weather
        weather = Weather(
            location_id=location.location_id,
            temperature=random.randint(50, 85),
            conditions=random.choice(list(WeatherCondition)),
            last_updated=datetime.utcnow(),
        )
        db.add(weather)
        db.commit()
        db.refresh(weather)

        print(f"✅ Added weather data for location {location.location_name}")

        # Generate hourly forecast
        for i in range(24):
            hourly_forecast = WeatherForecastHourly(
                weather_id=weather.weather_id,
                forecast_time=datetime.now() + timedelta(hours=i),
                forecast_temp=random.randint(40, 75),
                forecast_condition=random.choice(list(WeatherCondition)),
            )
            db.add(hourly_forecast)

        # Generate daily forecast for the next 10 days
        for i in range(10):
            daily_forecast = WeatherForecastDaily(
                weather_id=weather.weather_id,
                forecast_date=datetime.now() + timedelta(days=i),
                forecast_temp_high=random.randint(60, 80),
                forecast_temp_low=random.randint(40, 55),
                forecast_condition=random.choice(list(WeatherCondition)),
            )
            db.add(daily_forecast)

    db.commit()
    print("Mock weather data generated successfully!")

if __name__ == "__main__":
    db = SessionLocal()

    Base.metadata.create_all(bind=engine)  # ✅ Ensure tables exist before inserting data

    print("Generate locations")
    generate_mock_locations(db)

    print("Generate teams")
    generate_mock_teams(db)

    print("Generate users")
    generate_mock_users(db)

    print("Generate weather data")
    generate_weather_data(db)

    db.close()
    print("That's all folks!")

