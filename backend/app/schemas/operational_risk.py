from datetime import datetime

from pydantic import BaseModel

class RiskCreate(BaseModel):

    flight_id: int

    risk_type: str

    severity: str = "LOW"

    score: int = 0

    title: str

    description: str | None = None

class RiskUpdate(BaseModel):

    severity: str | None = None

    score: int | None = None

    title: str | None = None

    description: str | None = None

    status: str | None = None

class RiskResponse(BaseModel):

    id: int

    flight_id: int

    flight_number: str

    risk_type: str

    severity: str

    score: int

    title: str

    description: str | None

    status: str

    created_at: datetime

    resolved_at: datetime | None