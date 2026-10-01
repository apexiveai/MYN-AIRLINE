from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class BoardingPass(Base):

    __tablename__ = "boarding_passes"

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

    boarding_pass_number: Mapped[str] = mapped_column(

        String(40),

        unique=True,

        index=True,

        nullable=False,

    )

    gate: Mapped[str | None] = mapped_column(

        String(20),

        nullable=True,

    )

    boarding_group: Mapped[str | None] = mapped_column(

        String(20),

        nullable=True,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ISSUED",

    )

    issued_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    boarded_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    booking = relationship(

        "Booking",

        backref="boarding_pass",

    )