from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from security.security import get_api_key
from models.alerts import Alerts
from models.team import Team
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

# ✅ Get Weather Alerts for a Specific Location
@router.get("/{location_id}", summary="Get Active Weather Alerts for a Location")
def get_weather_alerts(location_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    """Fetch active weather alerts for teams in a given location."""

    # ✅ Find all teams associated with the location
    teams = db.query(Team.team_id).filter(Team.location_id == location_id).all()
    team_ids = [team.team_id for team in teams]

    if not team_ids:
        return {"message": "No teams found for this location"}

    # ✅ Get alerts for all teams in this location
    alerts = db.query(Alerts).filter(Alerts.team_id.in_(team_ids)).all()

    if not alerts:
        return {"message": "No active weather alerts"}

    return [
        {"alert_name": alert.alert_name, "alert_description": alert.alert_description}
        for alert in alerts
    ]

# ✅ Get All Alerts for the Past Hour
@router.get("/hourly", summary="Get Alerts for the Past Hour")
def get_hourly_alerts(db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    """Fetch all alerts issued in the last hour."""
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    alerts = db.query(Alerts).filter(Alerts.timestamp >= one_hour_ago).all()

    return {"alerts": alerts}

# ✅ Get All Alerts for Today
@router.get("/daily", summary="Get Alerts for Today")
def get_daily_alerts(db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    """Fetch all alerts issued since midnight UTC."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    alerts = db.query(Alerts).filter(Alerts.timestamp >= today_start).all()

    return {"alerts": alerts}
