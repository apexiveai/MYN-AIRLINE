from datetime import datetime

from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Crew(Base):

    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    employee_code: Mapped[str] = mapped_column(

        String(30),

        unique=True,

        index=True,

        nullable=False,

    )

    full_name: Mapped[str] = mapped_column(

        String(150),

        nullable=False,

    )

    role: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

    )

    license_number: Mapped[str | None] = mapped_column(

        String(80),

        unique=True,

        nullable=True,

    )

    base_airport: Mapped[str] = mapped_column(

        String(3),

        nullable=False,

    )

    status: Mapped[str] = mapped_column(

        String(30),

        nullable=False,

        default="AVAILABLE",

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