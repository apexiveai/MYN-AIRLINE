from datetime import datetime

from pydantic import BaseModel

class AircraftCreate(BaseModel):

    registration: str

    model: str

    manufacturer: str

    seat_capacity: int

    status: str = "AVAILABLE"

class AircraftUpdate(BaseModel):

    model: str | None = None

    manufacturer: str | None = None

    seat_capacity: int | None = None

    status: str | None = None

class AircraftResponse(BaseModel):

    id: int

    registration: str

    model: str

    manufacturer: str

    seat_capacity: int

    status: str

    total_flight_hours: float

    total_cycles: int

    last_maintenance_at: datetime | None

    next_maintenance_at: datetime | None

    model_config = {

        "from_attributes": True

    }