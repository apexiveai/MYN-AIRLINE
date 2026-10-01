from datetime import datetime

from pydantic import BaseModel

class WeatherCreate(BaseModel):

    airport_id: int

    temperature_c: float

    wind_speed_kmh: float

    wind_direction: int = 0

    visibility_km: float = 10

    precipitation_mm: float = 0

    cloud_cover: int = 0

    condition: str = "CLEAR"

    risk_level: str = "LOW"

class WeatherResponse(BaseModel):

    id: int

    airport_id: int

    iata_code: str

    airport_name: str

    temperature_c: float

    wind_speed_kmh: float

    wind_direction: int

    visibility_km: float

    precipitation_mm: float

    cloud_cover: int

    condition: str

    risk_level: str

    observed_at: datetime