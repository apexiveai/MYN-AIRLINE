from pydantic import BaseModel

class FlightCreate(BaseModel):

    flight_number: str

    origin: str

    destination: str

    aircraft: str

    gate: str | None = None

    status: str = "SCHEDULED"

    departure_time: str | None = None

    arrival_time: str | None = None

    latitude: float = 0

    longitude: float = 0

    altitude: int = 0

    speed: int = 0

    heading: float = 0

class FlightUpdate(BaseModel):

    origin: str | None = None

    destination: str | None = None

    aircraft: str | None = None

    gate: str | None = None

    status: str | None = None

    departure_time: str | None = None

    arrival_time: str | None = None

    latitude: float | None = None

    longitude: float | None = None

    altitude: int | None = None

    speed: int | None = None

    heading: float | None = None

class FlightResponse(BaseModel):

    id: int

    flight_number: str

    origin: str

    destination: str

    aircraft: str

    aircraft_registration: str | None

    gate: str | None

    status: str

    departure_time: str | None

    arrival_time: str | None

    latitude: float

    longitude: float

    altitude: int

    speed: int

    heading: float