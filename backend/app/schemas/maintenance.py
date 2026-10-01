from datetime import datetime

from pydantic import BaseModel

class MaintenanceCreate(BaseModel):

    aircraft_id: int

    maintenance_type: str

    description: str | None = None

    scheduled_start: datetime | None = None

    scheduled_end: datetime | None = None

    technician: str | None = None

class MaintenanceUpdate(BaseModel):

    maintenance_type: str | None = None

    status: str | None = None

    description: str | None = None

    scheduled_start: datetime | None = None

    scheduled_end: datetime | None = None

    actual_start: datetime | None = None

    actual_end: datetime | None = None

    technician: str | None = None

class MaintenanceResponse(BaseModel):

    id: int

    aircraft_id: int

    registration: str

    aircraft_model: str

    maintenance_type: str

    status: str

    description: str | None

    scheduled_start: datetime | None

    scheduled_end: datetime | None

    actual_start: datetime | None

    actual_end: datetime | None

    technician: str | None

    created_at: datetime