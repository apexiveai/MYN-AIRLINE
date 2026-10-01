from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class WeatherObservation(Base):

    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True,

    )

    airport_id: Mapped[int] = mapped_column(

        ForeignKey("airports.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    temperature_c: Mapped[float] = mapped_column(

        Float,

        nullable=False,

        default=0,

    )

    wind_speed_kmh: Mapped[float] = mapped_column(

        Float,

        nullable=False,

        default=0,

    )

    wind_direction: Mapped[int] = mapped_column(

        Integer,

        nullable=False,

        default=0,

    )

    visibility_km: Mapped[float] = mapped_column(

        Float,

        nullable=False,

        default=10,

    )

    precipitation_mm: Mapped[float] = mapped_column(

        Float,

        nullable=False,

        default=0,

    )

    cloud_cover: Mapped[int] = mapped_column(

        Integer,

        nullable=False,

        default=0,

    )

    condition: Mapped[str] = mapped_column(

        String(40),

        nullable=False,

        default="CLEAR",

    )

    risk_level: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        default="LOW",

    )

    observed_at: Mapped[datetime] = mapped_column(

        default=datetime.utcnow,

        index=True,

    )

    airport = relationship(

        "Airport",

        backref="weather_observations",

    )