from datetime import datetime

from pydantic import BaseModel

class TicketIssueCreate(BaseModel):

    booking_id: int

class TicketResponse(BaseModel):

    id: int

    booking_id: int

    ticket_number: str

    issue_status: str

    issued_at: datetime

    voided_at: datetime | None