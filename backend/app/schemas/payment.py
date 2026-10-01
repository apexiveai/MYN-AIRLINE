from datetime import datetime

from pydantic import BaseModel

class PaymentCreate(BaseModel):

    booking_id: int

    amount: float

    currency: str = "MMK"

    method: str = "CASH"

    provider: str | None = None

    transaction_id: str | None = None

class PaymentResponse(BaseModel):

    id: int

    booking_id: int

    amount: float

    currency: str

    method: str

    provider: str | None

    transaction_id: str | None

    status: str

    paid_at: datetime | None

    created_at: datetime