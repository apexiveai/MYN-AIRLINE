from datetime import datetime

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class CheckIn(Base):

    __tablename__ = "check_ins"

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

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="CHECKED_IN",

    )

    checkin_method: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="COUNTER",

    )

    checked_in_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    booking = relationship(

        "Booking",

        backref="checkin",

    )