from datetime import datetime

from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class OperationalAlert(Base):

    __tablename__ = "operational_alerts"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    flight_id: Mapped[int | None] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=True,

        index=True,

    )

    alert_type: Mapped[str] = mapped_column(

        String(40),

        nullable=False,

    )

    severity: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="INFO",

    )

    title: Mapped[str] = mapped_column(

        String(150),

        nullable=False,

    )

    message: Mapped[str] = mapped_column(

        Text,

        nullable=False,

    )

    status: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="OPEN",

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

        index=True,

    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    flight = relationship(

        "Flight",

        backref="operational_alerts",

    )