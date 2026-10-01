from datetime import datetime

from pydantic import BaseModel

class DisruptionCreate(BaseModel):

    flight_id: int

    disruption_type: str

    severity: str = "MEDIUM"

    reason: str

    description: str | None = None

class DisruptionUpdate(BaseModel):

    severity: str | None = None

    status: str | None = None

    reason: str | None = None

    description: str | None = None

    resolution: str | None = None

class DisruptionResponse(BaseModel):

    id: int

    flight_id: int

    flight_number: str

    disruption_type: str

    severity: str

    status: str

    reason: str

    description: str | None

    resolution: str | None

    created_at: datetime

    resolved_at: datetime | None