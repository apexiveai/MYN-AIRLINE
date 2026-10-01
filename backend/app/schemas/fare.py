from pydantic import BaseModel

class FareCreate(BaseModel):

    flight_id: int

    fare_code: str

    cabin_class: str = "ECONOMY"

    booking_class: str = "Y"

    base_fare: float

    taxes: float = 0

    currency: str = "MMK"

    seats_available: int = 0

class FareUpdate(BaseModel):

    base_fare: float | None = None

    taxes: float | None = None

    seats_available: int | None = None

    status: str | None = None

class FareResponse(BaseModel):

    id: int

    flight_id: int

    flight_number: str

    fare_code: str

    cabin_class: str

    booking_class: str

    base_fare: float

    taxes: float

    total_fare: float

    currency: str

    seats_available: int

    status: str