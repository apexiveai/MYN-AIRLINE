from datetime import datetime

from sqlalchemy import ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class OperationalRisk(Base):

    __tablename__ = "operational_risks"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    risk_type: Mapped[str] = mapped_column(

        String(40),

        nullable=False,

    )

    severity: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="LOW",

    )

    score: Mapped[int] = mapped_column(

        nullable=False,

        default=0,

    )

    title: Mapped[str] = mapped_column(

        String(150),

        nullable=False,

    )

    description: Mapped[str | None] = mapped_column(

        Text,

        nullable=True,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="OPEN",

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    resolved_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    flight = relationship(

        "Flight",

        backref="operational_risks",

    )