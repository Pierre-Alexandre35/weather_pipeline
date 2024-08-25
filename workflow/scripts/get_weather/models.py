
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90.")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180.")
    forecast_days: int = Field(default=None, ge=1, description="Forecast days must be a positive integer.")
