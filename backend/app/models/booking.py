from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Booking(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    pnr: Mapped[str] = mapped_column(

        String(6),

        unique=True,

        index=True,

        nullable=False,

    )

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    passenger_id: Mapped[int] = mapped_column(

        ForeignKey("passengers.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    booking_class: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

        default="Y",

    )

    fare_type: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ECONOMY",

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="CONFIRMED",

    )

    ticket_number: Mapped[str | None] = mapped_column(

        String(30),

        unique=True,

        nullable=True,

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    flight = relationship(

        "Flight",

        backref="bookings",

    )

    passenger = relationship(

        "Passenger",

        backref="bookings",

    )