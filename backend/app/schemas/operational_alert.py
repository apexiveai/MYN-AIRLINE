from datetime import datetime

from pydantic import BaseModel

class AlertUpdate(BaseModel):

    status: str | None = None

class AlertResponse(BaseModel):

    id: int

    flight_id: int | None

    flight_number: str | None

    alert_type: str

    severity: str

    title: str

    message: str

    status: str

    created_at: datetime

    acknowledged_at: datetime | None