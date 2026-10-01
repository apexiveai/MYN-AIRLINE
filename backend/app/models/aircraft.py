from datetime import datetime

from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Aircraft(Base):

    __tablename__ = "aircraft"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    registration: Mapped[str] = mapped_column(

        String(20),

        unique=True,

        index=True,

        nullable=False,

    )

    model: Mapped[str] = mapped_column(

        String(80),

        nullable=False,

    )

    manufacturer: Mapped[str] = mapped_column(

        String(80),

        nullable=False,

    )

    seat_capacity: Mapped[int] = mapped_column(

        nullable=False,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="AVAILABLE",

    )

    total_flight_hours: Mapped[float] = mapped_column(

        default=0,

        nullable=False,

    )

    total_cycles: Mapped[int] = mapped_column(

        default=0,

        nullable=False,

    )

    last_maintenance_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    next_maintenance_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )