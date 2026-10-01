from pydantic import BaseModel

class BookingCreate(BaseModel):

    flight_id: int

    passenger_id: int

    booking_class: str = "Y"

    fare_type: str = "ECONOMY"

class BookingUpdate(BaseModel):

    booking_class: str | None = None

    fare_type: str | None = None

    status: str | None = None

    ticket_number: str | None = None

class BookingResponse(BaseModel):

    id: int

    pnr: str

    flight_id: int

    flight_number: str

    passenger_id: int

    passenger_name: str

    booking_class: str

    fare_type: str

    status: str

    ticket_number: str | None

    seat_number: str | None