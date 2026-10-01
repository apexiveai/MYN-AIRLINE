from datetime import datetime

from sqlalchemy import Float, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Baggage(Base):

    __tablename__ = "baggage"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    booking_id: Mapped[int] = mapped_column(

        ForeignKey("bookings.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    bag_tag: Mapped[str] = mapped_column(

        String(30),

        unique=True,

        index=True,

        nullable=False,

    )

    weight_kg: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )

    bag_type: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="CHECKED",

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="ACCEPTED",

    )

    scanned_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    booking = relationship(

        "Booking",

        backref="baggage_items",

    )