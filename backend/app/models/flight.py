from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    flight_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    origin_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id"),
        nullable=False,
    )

    destination_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id"),
        nullable=False,
    )

    aircraft_id: Mapped[int | None] = mapped_column(
        ForeignKey("aircraft.id"),
        nullable=True,
    )

    gate: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="SCHEDULED",
    )

    departure_time: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    arrival_time: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    altitude: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    speed: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    heading: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
    )

    origin = relationship(
        "Airport",
        foreign_keys=[origin_id],
    )

    destination = relationship(
        "Airport",
        foreign_keys=[destination_id],
    )

    aircraft = relationship(
        "Aircraft",
        foreign_keys=[aircraft_id],
    )