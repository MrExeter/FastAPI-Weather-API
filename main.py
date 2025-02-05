from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
from database.database import Base, engine
from routes.weather_routes import router as weather_router
from routes.auth_routes import router as auth_router
from routes.team_routes import router as team_router
from routes.alerts_route import router as alerts_router


app = FastAPI()


# Initialize Database
Base.metadata.create_all(bind=engine)

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

@app.get("/", summary="Root Endpoint")
def home():
    return {"message": "Hello World! Weather API is running"}

# Register routes
app.include_router(weather_router)
app.include_router(auth_router)
app.include_router(team_router)
app.include_router(alerts_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
