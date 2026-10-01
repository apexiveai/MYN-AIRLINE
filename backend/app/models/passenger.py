from datetime import datetime

from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Passenger(Base):

    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    passenger_code: Mapped[str] = mapped_column(

        String(30),

        unique=True,

        index=True,

        nullable=False,

    )

    first_name: Mapped[str] = mapped_column(

        String(100),

        nullable=False,

    )

    last_name: Mapped[str] = mapped_column(

        String(100),

        nullable=False,

    )

    gender: Mapped[str | None] = mapped_column(

        String(20),

        nullable=True,

    )

    date_of_birth: Mapped[str | None] = mapped_column(

        String(20),

        nullable=True,

    )

    nationality: Mapped[str | None] = mapped_column(

        String(80),

        nullable=True,

    )

    passport_number: Mapped[str | None] = mapped_column(

        String(50),

        unique=True,

        nullable=True,

    )

    phone: Mapped[str | None] = mapped_column(

        String(30),

        nullable=True,

    )

    email: Mapped[str | None] = mapped_column(

        String(150),

        nullable=True,

    )

    created_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

    )