from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Ticket(Base):

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    booking_id: Mapped[int] = mapped_column(

        ForeignKey("bookings.id", ondelete="CASCADE"),

        unique=True,

        nullable=False,

        index=True,

    )

    ticket_number: Mapped[str] = mapped_column(

        String(30),

        unique=True,

        nullable=False,

        index=True,

    )

    issue_status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ISSUED",

    )

    issued_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    voided_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    booking = relationship(

        "Booking",

        backref="ticket",

    )