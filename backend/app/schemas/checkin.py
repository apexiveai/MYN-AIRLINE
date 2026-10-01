from datetime import datetime

from pydantic import BaseModel

class CheckInCreate(BaseModel):

    booking_id: int

    checkin_method: str = "COUNTER"

class CheckInResponse(BaseModel):

    id: int

    booking_id: int

    status: str

    checkin_method: str

    checked_in_at: datetime