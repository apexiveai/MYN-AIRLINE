from datetime import datetime

from sqlalchemy import Float, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Fare(Base):

    __tablename__ = "fares"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    fare_code: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        index=True,

    )

    cabin_class: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="ECONOMY",

    )

    booking_class: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

        default="Y",

    )

    base_fare: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )

    taxes: Mapped[float] = mapped_column(

        Float,

        nullable=False,

        default=0,

    )

    currency: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

        default="MMK",

    )

    seats_available: Mapped[int] = mapped_column(

        nullable=False,

        default=0,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ACTIVE",

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    flight = relationship(

        "Flight",

        backref="fares",

    )