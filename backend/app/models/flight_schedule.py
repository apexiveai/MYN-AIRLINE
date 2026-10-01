from datetime import datetime, date, time

from sqlalchemy import Date, ForeignKey, String, Time

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class FlightSchedule(Base):

    __tablename__ = "flight_schedules"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    operating_date: Mapped[date] = mapped_column(

        Date,

        nullable=False,

        index=True,

    )

    scheduled_departure: Mapped[time] = mapped_column(

        Time,

        nullable=False,

    )

    scheduled_arrival: Mapped[time] = mapped_column(

        Time,

        nullable=False,

    )

    actual_departure: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    actual_arrival: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="SCHEDULED",

    )

    delay_minutes: Mapped[int] = mapped_column(

        default=0,

        nullable=False,

    )

    flight = relationship(

        "Flight",

        backref="schedules",

    )