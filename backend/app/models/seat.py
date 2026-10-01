from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class SeatAssignment(Base):

    __tablename__ = "seat_assignments"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    booking_id: Mapped[int] = mapped_column(

        ForeignKey("bookings.id", ondelete="CASCADE"),

        unique=True,

        nullable=False,

        index=True,

    )

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    seat_number: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

    )

    cabin_class: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="ECONOMY",

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ASSIGNED",

    )

    assigned_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    booking = relationship(

        "Booking",

        backref="seat",

    )

    flight = relationship(

        "Flight",

        backref="seat_assignments",

    )