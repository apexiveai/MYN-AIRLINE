from pydantic import BaseModel

class SeatAssignCreate(BaseModel):

    booking_id: int

    seat_number: str

    cabin_class: str = "ECONOMY"

class SeatResponse(BaseModel):

    id: int

    booking_id: int

    flight_id: int

    seat_number: str

    cabin_class: str

    status: str