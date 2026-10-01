from datetime import datetime

from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class MaintenanceRecord(Base):

    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    aircraft_id: Mapped[int] = mapped_column(

        ForeignKey("aircraft.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    maintenance_type: Mapped[str] = mapped_column(

        String(40),

        nullable=False,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="SCHEDULED",

    )

    description: Mapped[str | None] = mapped_column(

        Text,

        nullable=True,

    )

    scheduled_start: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    scheduled_end: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    actual_start: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    actual_end: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    technician: Mapped[str | None] = mapped_column(

        String(150),

        nullable=True,

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    aircraft = relationship(

        "Aircraft",

        backref="maintenance_records",

    )