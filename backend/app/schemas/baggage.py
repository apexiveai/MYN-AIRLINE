from datetime import datetime

from pydantic import BaseModel

class BaggageCreate(BaseModel):

    booking_id: int

    weight_kg: float

    bag_type: str = "CHECKED"

class BaggageResponse(BaseModel):

    id: int

    booking_id: int

    bag_tag: str

    weight_kg: float

    bag_type: str

    status: str

    scanned_at: datetime