from datetime import datetime

from pydantic import BaseModel

class BoardingPassCreate(BaseModel):

    booking_id: int

    gate: str | None = None

    boarding_group: str | None = None

class BoardingPassResponse(BaseModel):

    id: int

    booking_id: int

    boarding_pass_number: str

    gate: str | None

    boarding_group: str | None

    status: str

    issued_at: datetime

    boarded_at: datetime | None