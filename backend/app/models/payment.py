from datetime import datetime

from sqlalchemy import Float, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Payment(Base):

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    booking_id: Mapped[int] = mapped_column(

        ForeignKey("bookings.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    amount: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )

    currency: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

        default="MMK",

    )

    method: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="CASH",

    )

    provider: Mapped[str | None] = mapped_column(

        String(50),

        nullable=True,

    )

    transaction_id: Mapped[str | None] = mapped_column(

        String(100),

        unique=True,

        nullable=True,

        index=True,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="PENDING",

    )

    paid_at: Mapped[datetime | None] = mapped_column(

        nullable=True,

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )

    booking = relationship(

        "Booking",

        backref="payments",

    )