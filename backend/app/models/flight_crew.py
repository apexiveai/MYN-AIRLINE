from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class FlightCrew(Base):

    __tablename__ = "flight_crew"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    flight_id: Mapped[int] = mapped_column(

        ForeignKey("flights.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    crew_id: Mapped[int] = mapped_column(

        ForeignKey("crew.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    duty_role: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

    )

    assigned_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    flight = relationship(

        "Flight",

        backref="crew_assignments",

    )

    crew = relationship(

        "Crew",

        backref="flight_assignments",

    )