from datetime import date, datetime, time

from pydantic import BaseModel

class FlightScheduleCreate(BaseModel):

    flight_id: int

    operating_date: date

    scheduled_departure: time

    scheduled_arrival: time

class FlightScheduleUpdate(BaseModel):

    scheduled_departure: time | None = None

    scheduled_arrival: time | None = None

    actual_departure: datetime | None = None

    actual_arrival: datetime | None = None

    status: str | None = None

    delay_minutes: int | None = None

class FlightScheduleResponse(BaseModel):

    id: int

    flight_id: int

    flight_number: str

    origin: str

    destination: str

    operating_date: date

    scheduled_departure: time

    scheduled_arrival: time

    actual_departure: datetime | None

    actual_arrival: datetime | None

    status: str

    delay_minutes: int